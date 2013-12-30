//基于Script的跨域SRV调用 Cross-site SRV
if(typeof IO == 'undefined' )IO = {};
IO.XSRV2 = function(){
	this.Init.apply(this, arguments);
}; 
IO.XSRV2.CallbackList = [];
IO.XSRV2.prototype = {
	_url : null,
	_err_cb : null,
	_loader : null,
	Init : function(a_ServiceURL, a_ErrorCB, a_randomURL){
		var l_opt = {};
		var o;
		this._err_cb = a_ErrorCB;
		this._url = a_ServiceURL;
		o = document.getElementById('divLoader');
		if (o)
		{
			this._loader = o;
		}
		else
		{
			this._loader = document.body;
		}
		this._randUrl = a_randomURL;
	},
	jshash : function (s)
	{
		var a, i, j, c, c0, c1, c2, r;
		var _s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_$';
		var _r64 = function(s, b)
		{
			return ((s | (s << 6)) >>> (b % 6)) & 63;
		};
		a = [];
		c = [];
		for (i = 0; i < s.length; i++)
		{
			c0 = s.charCodeAt(i);
			if (c0 & ~255)
			{
				c0 = (c0 >> 8) ^ c0;
			}
			c.push(c0);
			if (c.length == 3 || i == s.length - 1)
			{
				while(c.length < 3)
				{
					c.push(0);
				}
				a.push((c[0] >> 2) & 63);
				a.push(((c[1] >> 4) | (c[0] << 6)) & 63);
				a.push(((c[1] << 4) | (c[2] >> 2)) & 63);
				a.push(c[2] & 63);
				c = [];
			}
		}
		while (a.length < 16)
		{
			a.push(0);
		}
		r = 0;
		for (i = 0; i < a.length; i++)
		{
			r ^= (_r64(a[i] ^ (r | i), i) ^ _r64(i, r)) & 63;
		}
		for (i = 0; i < a.length; i++)
		{
			a[i] = (_r64((r | i & a[i]), r) ^ a[i]) & 63;
			r += a[i];
		}
		for (i = 16; i < a.length; i++)
		{
			a[i % 16] ^= (a[i] + (i >>> 4)) & 63;
		}
		for (i = 0; i < 16; i++)
		{
			a[i] = _s.substr(a[i], 1);
		}
		a = a.slice(0, 16).join('');
		return a;
	},
	Call : function(a_srvname, a_callback, a_arguments, a_cid){
		var a = [];
		for (var k in a_arguments)
		{
			a.push(encodeURIComponent(k) + '=' + encodeURIComponent(a_arguments[k]));
		}
		if (this._randUrl)
		{
			a.push(encodeURIComponent(this._randUrl) + '=' + Math.floor(60466176 * Math.random()).toString(36));
		}
		a = a.join('&');
		var h, s, i;
		s = a_srvname + '?' + a;
		if (a_cid && a_cid !== true)
		{
			h = cid;
		}
		else
		{
			h = this.jshash(s);
			for (i = 0; IO.XSRV2.CallbackList[h] ; i++)
			{
				h = this.jshash(s + '#@`' + i);
			}
		}
		var l_load_path = this._url + '/' +
		   		'IO.XSRV2.CallbackList[\'' + h  + '\']' + '/' + a_srvname;
		if (a)
		{
			l_load_path += '?' + a;
		}
		var l_el= document.createElement("script");
		l_el.type = "text/javascript";
		l_el.src = l_load_path;
		IO.XSRV2.CallbackList[h] = function(a_data) {
		    setTimeout(function()
		    {
			    document.getElementById('divLoader').removeChild(l_el);
			    l_el = null;
			    a_callback(a_data, h);
			    delete IO.XSRV2.CallbackList[h];
			},0);
		};
		setTimeout(function()
		{
		    document.getElementById('divLoader').appendChild(l_el);
		},0);
	}
};
