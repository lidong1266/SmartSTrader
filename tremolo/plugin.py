#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os, inspect

def get_subclass(dirPath, baseCls):
    '''
    指定されたディレクトリパス以下に存在するbaseClsのサブクラスのみを取得し、
    リストで返す.

    path:
        処理対象ディレクトリ
    baseClass:
        基底クラスオブジェクト

    RETURN:
        クラスのリスト.
    '''
    clsSet = set()

    for p in os.listdir(dirPath):
        itemPath = os.path.join(dirPath, p)
        if os.path.isfile(itemPath):
            fname, ext = os.path.splitext(p)
            if ext not in ['.py', '.pyc']:
                continue
            if fname == '__init__':
                continue
            
            # モジュール名を取得
            modName = inspect.getmodulename(itemPath)
            if not modName:
                continue
            modDir = os.path.split(dirPath)[1]
            if not modDir:
                continue
            
            # モジュールをインポートする
            print '.'.join([modDir, modName])
            mod = __import__('.'.join([modDir, modName]))
            mod = getattr(mod, modName)

            # クラスの抽出
            for name, cls in inspect.getmembers(mod, inspect.isclass):
                # 指定されたベースクラス自身、またはモジュール内でインポート
                # されているクラスの場合には無視.
                if cls == baseCls or inspect.getmodule(cls) != mod:
                    continue

                # ベースクラスのサブクラスでない場合には無視.
                if not issubclass(cls, baseCls):
                    continue
                clsSet.add(cls)
            del mod
        elif os.path.isdir(itemPath):
            for cls in get_subclass(itemPath, baseCls):
                clsSet.add(cls)
        else:
            pass

    return list(clsSet)
