# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:46:06 2015

@author: PAVILION
"""
import io
import base64

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import LogLocator

from bottle import Bottle, run, response, static_file, request, route, template, default_app

app = Bottle()

# Generate ticks
def weibull_CDF(y, pos):
    return "%G %%" % (100*(1-np.exp(-np.exp(y))))

def percent_print(y, pos):
    return "%G %%" % (100*y)
    
y_formatter = FuncFormatter(weibull_CDF)
y_formatter2 = FuncFormatter(percent_print)
x_formatter = FuncFormatter(lambda x, pos: np.exp(x))
x_locator = LogLocator(2)

import scipy.stats as stats # scipy is a statistical package for Python
# Use Scipy's stats package to perform least-squares fit

def plot_pdf(t, loc, scale, shape, output):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.yaxis.set_major_formatter(y_formatter2)
    #ax.yaxis.set_major_formatter(x_formatter)
    
    y = weib_pdf(t, loc, scale, shape)
    ax.scatter(t, y)

    xt_F = np.logspace(np.ceil(np.log10(loc)), np.ceil(np.log10(t.max())), 100)
    yt_F = weib_pdf(xt_F, loc, scale, shape)
    ax.set_xscale('log')
    ax.set_xlim([1, xt_F.max()])
    ax.set_ylim([0, yt_F.max()])
    ax.plot(xt_F, yt_F)
    
    plt.grid()
    ax.set_title("Weibull Probability Density Function", weight='bold')
    fig.savefig(output, format="png");
    output.seek(0)
    

def plot_linreg(x,y, output, draw_line=False):
    """
    return shape, slope, r_value
    """
    # y = slope * x + intercept
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    yt_F = np.array([ 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5,
           0.6, 0.7, 0.8, 0.9, 0.95, 0.99])
    yt_lnF = np.log(-np.log(1-yt_F))
    xt_F = np.power(10, np.arange(8))
    xt_lnF = np.log(xt_F)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_yticks(yt_lnF)
    ax.set_xticks(xt_lnF)
    ax.yaxis.set_major_formatter(y_formatter)
    ax.xaxis.set_major_formatter(x_formatter)
    #ax.xaxis.set_major_locator(x_locator)
    plt.xlim(1)
    ax.scatter(x, y)
    if draw_line:
        line = slope*x+intercept
        ax.plot(x, line)
        ax.set_title("Weibull Cumulative Distribution Function\nLinear Regression - Least Squares Method", weight='bold')
    else:
        ax.set_title("Weibull Cumulative Distribution Function", weight='bold')
    plt.grid()
    fig.savefig(output,format="png");
    output.seek(0)
    #print("R^2: {}".format(r_value**2))
    #print("Shape:{} Scale:{}".format(slope, np.exp(-intercept/slope)))
    return slope, np.exp(-intercept/slope), r_value

def weib_pdf(t, loc, scale, shape):
    return (shape/scale)*(((t-loc)/scale)**(shape-1))*((np.exp(-((t-loc)/scale)))**shape)
    
def reliability(t, loc, scale, shape):
    return (np.exp(-((t - loc)/scale)**shape))

def reliable_life(r, loc, scale, shape):
    return (loc + (scale*((-np.log(r))**(1/shape))))

def median_rank(n):
    return (np.arange(1, n+1)-0.3)/(n+0.4)

#calculate location (t0_hat) by way of Zanakis [1992]
def p(n):
    return (0.8829*n**(-0.3437))

def t0_hat(x):
    n = len(x) - 1
    j = np.ceil(n * p(n)) - 1
    t1 = x[0]
    tn = x[n]
    tj = x[j]

    return (t1*tn-tj**2)/(t1 + tn - 2*tj)

def weibull_scale_transform(data):
    x = np.log(data)
    y = np.log(-np.log(1 - median_rank(len(data))))
    return x, y

@route("/relia", method="POST")
def relia():
    shape= float(request.forms.get('shape'))
    scale= float(request.forms.get('scale'))
    t0= float(request.forms.get('loc'))
    if request.query.inv == "1":
        r = float(request.forms.get("reliability"))
        content = "{}".format(reliable_life(r, t0, scale, shape))
    else:
        tfail = float(request.forms.get("tfail"))
        content = "{}".format(reliability(tfail, t0, scale, shape))

    
    return content

@route("/fitting", method='POST')
def fitting():
    #tfail = np.loadtxt("Fail_data.csv")
    if request.query.upload == "1":
        input_data = request.files.inputfile.file
    else:
        input_data = io.StringIO(request.forms.get("inputdata"))

    tfail = np.loadtxt(input_data)
    x1, y1 = weibull_scale_transform(tfail)
    t0 = t0_hat(tfail)
    x2, y2 = weibull_scale_transform(tfail - t0)

    output1 = io.BytesIO()
    output2 = io.BytesIO()
    output3 = io.BytesIO()
    
    shape1, scale1, r_value1 = plot_linreg(x1,y1, output1)
    #print ("Reliability: {}".format (reliability(tfail, 0, scale1, shape1)))
    shape2, scale2, r_value2 = plot_linreg(x2,y2, output2, draw_line=True)
    plot_pdf(tfail, t0, scale2, shape2, output3)
    r = reliability(tfail, t0, scale2, shape2)
    #print ("Location:{}".format(t0))
    #print ("Reliability: {}".format (reliability(tfail, t0, scale2, shape2)))
    #print ("Reliable Life: {}".format (reliable_life(r,t0, scale2, shape2)))

    html = """<html><body>
        
    <table border="0">
        <tr>
            <td width="57%">
                <img src="data:image/png;base64,{0}"/>
                
                <img src="data:image/png;base64,{6}"/>
            </td>
            <td valign="top" width="43%">
                R^2 = {2} <br>
                Shape Parameter = {3} <br>
                Scale Parameter = {4} <br>
                Location Parameter = {5} <br>
                
                Reliability: <input id ="reliability" name="reliability" type='text' />
                <input value="Hitung Reliable Life" id= "hitung_reliablelife" type='submit' />
                <input id="shape" name="shape" value="{3}" type='hidden' />
                <input  id="scale" name="scale" value="{4}" type='hidden' />
                <input  id="loc" name="loc" value="{5}" type='hidden' />
                <br>
                Reliable Life: <input  id="tfail" name="tfail" type='text' />
                <input value="Hitung Reliability" type='submit' id="hitung_reliability" />
            </td>
        </tr>
    </table>
    
     
    <script type="text/javascript" src="/static/js/jquery.min.js"></script>
    <script type="text/javascript" src="/static/js/scripts.js"></script>
    </body>
    </html>""".format(base64.encodebytes(output1.getvalue()).decode(),
            base64.encodebytes(output2.getvalue()).decode(),
            (r_value2**2),
            shape2,
            scale2,
            t0,
            base64.encodebytes(output3.getvalue()).decode())
    plt.close()
    return html


@route("/")
def index():
    return template('template')

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/views/')) 

application=default_app()

#test_calc()
#run(host ='localhost', port=8080, debug=False)
