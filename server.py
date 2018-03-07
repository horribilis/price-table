import os
from os import listdir
from os.path import isfile, join
import time
from PIL import Image
from flask import send_file, request, app
import sys
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib.ft2font import FT2Font
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import six
import pandas as pd
from six import unichr
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/price/<string:uid>/<string:content>')
def price(uid,content):
    labelc = ['Part', 'Damaged-Level', 'Price']
    chars = []
    ivaa_case = uid
    print(ivaa_case)
    rows = content.split(",,")
    f = open("res/"+uid+".csv","w")
    if len(rows)==2 and content.split(",,")[1]=='':
        a = str(content.split(",,")[0].split(",")[0])
        b = str(content.split(",,")[0].split(",")[1])
        c = str(content.split(",,")[0].split(",")[2])
        f.write(a+","+b+","+c+"\n")
    else:
        for i in rows:
            a = str(i.split(",")[0])
            b = str(i.split(",")[1])
            c = str(i.split(",")[2])
            print(a)
            f.write(a+","+b+","+c+"\n")
    f.close()
    df = pd.read_csv("res/"+uid+".csv",header=None)
    for i in range(len(df.index)):
        print(type(df.iloc[i]))
        chars.append(df.iloc[i])
    print(chars)
    labelr = []
    for i in range(len(df.index)):
        labelr.append(" "+str(i+1))
    colors = [[(0.95, 0.95, 0.95) for c in range(3)] for r in range(len(df.index))]
    print("aaa")
    plt.title('CASE-ID : '+ivaa_case)
    print("bbb")
    print(chars)
    print(labelr)
    print(labelc)
    print(colors)
    plt.table(cellText=chars,
                rowLabels=labelr,
                colLabels=labelc,
                rowColours=[(1,1,1)] * len(df.index),
                colColours=[(0.5,0.5,1)] * 3,
                cellColours=colors,
                cellLoc='center',
                loc='upper left')
    print("ccc")
    price = 0
    for i in range(len(df.index)):
        price = price + float(df.iloc[i][2])
    plt.text(0.3, 0.05, 'Estimated Total price is '+str(price)+' Bath.',fontsize=15)
    plt.axis('off')
    plt.savefig('res/'+ivaa_case+'.png')
    print("zzzz")
    return send_file('res/'+ivaa_case+'.png', mimetype='image/jpg')
    # parts = str(request.args.get('parts')).split(',')
    # side = request.args.get('side')
    # if not side:
    #     return
    # filename = gen_side(parts, side)
    # return send_file(filename, mimetype='image/jpg')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
