// javascript document
// work with stock_list.js
var markets = { 'NYSE': 'ŦԼ������','NASDAQ': '��˹���','AMEX': '����������' };
S_SL_PH = function(){
	this.Init.apply(this, arguments);
};

S_SL_PH.prototype = {
    Init: function (f)
    {
        this._frame = f;
        this.svcParam = { page: 1,num: 20,sort: '',asc: 0,market: '',id: ''};
        this.css = { up: 'green',down: 'red',highlight: 'highlight',
            sortasc: 'sort_up',sortdesc: 'sort_down',
            pagediv: 'pages',pagedisabled: 'pagedisabled',pagecurr: 'pagecurr'
        };
        this.aRowCss = ['','row_2'];
        this.outputParam = ['sort','page','num','asc'];
        this.colorfield = 4;
        this.pagetags = 5;
        //��ǰ׺��css
        this.tmrInt = 60000;
        this.tmrCntFull = 1;
        //�б�f=�ֶ�����t=��ʾ��/�ֶα��⣬d=С��λ����-1�������ã�-2��ʾ�ַ���
        //s: 1=��ʾ�������� 2=���������� 4=ǿ��+�� 8=ǧλ���� 16=ʹ��th 32=Ĭ�ϵ��� 64=�ǵ���ͷ
        //   128=innerHTML/DOM
        //c: custom_css
        //p: template
        this.aFields = [
		  { f: 'icname',t: '����',d: -2,s: 1 + 2,c: 'nocolor max_name' },
		  { f: 'symbol',t: '����',d: -2,s: 1 + 2,c: 'nocolor' },
		  { f: 'newprice',t: '�̺��',d: 2,s: 8 + 16,c: ' nocolor' },
		  { f: 'newdiff',t: '�ǵ���',d: 2,s: 4 + 8 + 16,c: 'text_right' },
		  { f: 'newchg',t: '�ǵ���',d: 2,s: 4 + 8 + 16, c: '' },
		  { f: 'newclose',t: '���ռ�',d: 2,s:  2 + 8 + 16,c: ' nocolor' },
		  { f: 'newvolume',t: '�̺�ɽ���',d: 0,s: 2 +  8 + 16,c: 'nocolor' },
		  { f: 'volume',t: '���ճɽ���',d: 0,s:  2 + 8 + 16,c: 'nocolor' },
		  { f: 'newustime',t: '����ʱ��',d: -2,s:0,c: 'nocolor' },
		  { f: 'mktcap',t: '��ֵ���ڣ�',d: 2,s: 2 + 8 + 16,c: 'nocolor' },
		  { f: 'pe',t: '��ӯ��',d: 2,s: 8 + 16,c: 'nocolor' },
		  { f: 'category',t: '��ҵ���',d: 2,s: 2 +  1,c: 'nocolor max_name' },
		  { f: 'instown', t: '�����ֹ�',d : 2,s :0, c:'nocolor'},
		  { f: 'beta', t: 'Betaֵ', d : 2, s : 2, c : 'nocolor'},
		  { f: 'avgvol', t: '10�վ���', d: 0, s:  2 + 8 + 16, c: 'nocolor'},
		  { f: 'eps', t: 'ÿ������', d: 2, s: 2, c: 'nocolor'},
		  { f: 'shares', t: '�ɱ�����', d: 2, s:  2 + 8, c: 'nocolor'},
		  { f: 'dividend', t: '��Ϣ', d: 2, s: 2, c: 'nocolor'},
		  { f: 'yield', t: '������', d: 2, s: 2, c: 'nocolor'},
		  { f: 'market',t: '��Ʊ���е�',d: -2,s:2,c: 'nocolor' }
		];
        this.indexField = 'symbol';
        this.detailPage = 'http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=$1&country=usstock';
        this._aCodes = [];
        this._srv = this._frame.SRVProvider();
    },
    GetData: function (cb)
    {
        getScript('http://hq.sinajs.cn/rn=' + random() + '&list=gb_dji',function ()
        {
            var _time = hq_str_gb_dji.split(',')[25];
            _time = _time.replace('AM',' ����').replace('PM',' ����');
            _time = _time.split(' ');
            if(_time[3] == '����')
            {
                var _tmp = _time[2].split(':');
                if(_tmp[0] == 12)
                {
                    _tmp[0] -= 12;
                }
                _time[2] = _tmp[0] - -12 + ':' + _tmp[1];
            }
            //	        if(parseInt(_time[2]) - 16 >= 0)
            //	        {
            //	            _time[2] = '16:00';
            //	        }
            var _mon = { Jan: 1,Feb: 2,Mar: 3,Apr: 4,May: 5,Jun: 6,Jul: 7,Aug: 8,Sep: 9,Oct: 10,Nov: 11,Dec: 12 };
            document.getElementById('updateTime').innerHTML = _mon[_time[0]] + '��' + _time[1] + '�� ' + _time[2];
        });
        this._cbSVC = cb;
        //��֧�ֲ����һص���ͬ�������ʵ����û���������
        this._frame.SRVCall('US_DataCenterService.getAfterData',this._gotData._Bind(this),this.svcParam);
    },
    _gotData: function (o)
    {
        o = o || {
			count : 0,
			data : []
		};
        this.cb(o.count);
        this._cbSVC(this._makeData(o.data));
    },
    GetDataLight: function ()
    {
    },
    GetListLength: function (cb)
    {
        this.cb = cb;
    },
    CodesChange: function (c)
    {
        this._aCodes = c;
        if(this._oQDL)
        {
            this._oQDL.changeCodes(c);
        }
    },
    _makeData: function (argData)
    {
        for(var i = 0;i < argData.length;i++)
        {
            //            if(argData[i].market != 'A')
            //            {
            //                argData[i].market = _marketType[argData[i].market];
        	//            }
        	argData[i].icname = argData[i].icname || argData[i].symbol;
			argData[i].newclose = argData[i].newprice - argData[i].newdiff;
			argData[i].newustime = (argData[i].newustime || '').split(/\s+/)[1] || '';
            var _name = document.createElement('a');
            _name.href = 'http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=$1&country=usstock'.replace('$1',argData[i].symbol);
            _name.target = '_blank';
            _name.innerHTML = argData[i].icname;
            _name.title = argData[i].icname;
            argData[i].icname = _name;
            if(argData[i].preclose * 1 > 10000)
            {
                argData[i].preclose = Math.round(argData[i].preclose * 1);
            }
            if(argData[i].open * 1 > 10000)
            {
                argData[i].open = Math.round(argData[i].open * 1);
            }
            if(argData[i].high * 1 > 10000)
            {
                argData[i].high = Math.round(argData[i].high * 1);
            }
            if(argData[i].low * 1 > 10000)
            {
                argData[i].low = Math.round(argData[i].low * 1);
            }
            argData[i].shou_kai = argData[i].preclose + '/' + argData[i].open;
            argData[i].gao_di = argData[i].high + '/' + argData[i].low;

            argData[i].mktcap = argData[i].mktcap / 100000000;
            if(argData[i].turnover === null)
            {
                var _span = document.createElement('span');
                _span.innerHTML = '--';
                argData[i].turnover = _span;
            }
            if(argData[i].mktcap == 0)
            {
                var _span = document.createElement('span');
                _span.innerHTML = '--';
                argData[i].mktcap = _span;
            }
            var _cate = document.createElement('a');
            _cate.href = 'javascript:void(0);';
            _cate.onclick = selectCate.bindArg(argData[i].industry_id);
            _cate.innerHTML = argData[i].category || '';
            _cate.title = argData[i].category;
            argData[i].category = _cate;
            if(markets[argData[i].market])
            {
                var _market = document.createElement('a');
                _market.href = 'javascript:void(0);';
                _market.onclick = dataCtrl.select.fnBind(dataCtrl,[undefined,{ 'NYSE': 'N','NASDAQ': 'O','AMEX': 'A'}[argData[i].market]]);
                _market.innerHTML = markets[argData[i].market] || argData[i].market;
                argData[i].market = _market;
            }
            else
            {
                argData[i].market = markets[argData[i].market] || argData[i].market;
            }
            if(argData[i].pe <= 0){
                argData[i].pe = '--';
            }

			if(argData[i].instown <= 0){
				argData[i].instown = '--'
			}else{
				argData[i].instown = (argData[i].instown * 100).toFixed(2) + '%';
			}
			if(argData[i].beta == 0){
				argData[i].beta = '--';
			}
			if(argData[i].eps == 0){
				argData[i].eps = '--';
			}
			if(argData[i].dividend == 0){
				argData[i].dividend = '--';
			}
			if(argData[i].yield == 0){
				argData[i].yield = '--';
			}else{
				argData[i].yield = argData[i].yield + '%';
			}
			if(argData[i].shares == 0){
				argData[i].shares = '--';
			}else{
				argData[i].shares = argData[i].shares / 1e4;
			}
			if(argData[i].newprice <= 0){
				argData[i].newprice = '--';
				argData[i].newdiff = '--';
				argData[i].newchg = '--';
			}else if(argData[i].newchg < 0){
				argData[i].newchg = (argData[i].newchg - 0).toFixed(2) + '%';
			}else{
				argData[i].newchg = '+' + (argData[i].newchg - 0).toFixed(2) + '%';
			}
        }
        return argData;
    }
};
