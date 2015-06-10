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
    
    if ((loc+t.min())/2 > 0):
        xt_F = np.logspace(np.log10((loc+t.min())/2), np.log10(t.max()*10), 100)
    else:
        xt_F = np.logspace(np.log10(t.min()), np.log10(t.max()*10), 100)
    yt_F = weib_pdf(xt_F, loc, scale, shape)
    
    if (np.any(np.isfinite(y))):
        ax.set_xscale('log')
    
    #ax.set_xlim([1, xt_F.max()])
    ax.set_ylim([0, yt_F.max()*2])
    ax.set_xlabel('Age (T), log scale')
    ax.set_ylabel('Weibull PDF')
    ax.plot(xt_F, yt_F)
    
    plt.grid()
    ax.set_title("Weibull probability density function (pdf)", weight='bold')
    fig.savefig(output, format="png")
    plt.close(fig)
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
    ax.set_xlabel('Age (T), log scale')
    ax.set_ylabel('Median Rank, % scale')
    #ax.set_xlim(left=0)
    ax.set_ylim([yt_lnF.min(), yt_lnF.max()])
    ax.scatter(x, y)
    if draw_line:
        line = slope*x+intercept
        ax.plot(x, line)
        ax.set_title("Weibull Cumulative Distribution Function\nLinear Regression - Least Squares Method", weight='bold')
    else:
        ax.set_title("Weibull Cumulative Distribution Function", weight='bold')
    plt.grid()
    fig.savefig(output,format="png")
    plt.close(fig)
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

def median_rank(n, N):
    """
    n: number of failure
    N: number of sample (failure + survivor)
    """
    return (np.arange(1, n+1)-0.3)/(N+0.4)

#calculate location (t0_hat) by way of Zanakis [1992]
def p(n): #p for weibull dist
    return (0.8829*n**(-0.3437))


def t0_test(t, n):
    t_complete = t.copy()
    t_complete.sort()
    t_fail = t_complete[:n]
    
    t0 = (t_fail.min() * t_fail.max() - t_fail**2)/(t_fail.min() + t_fail.max() - 2 * t_fail)
    return t0

def t0_hat(x, N):
    n = len(x)
    j = np.ceil(n * p(n) * n / N)
    t1 = x[0]
    tn = x[n - 1] #python index starts from 1
    tj = x[j - 1]

    t0 = (t1*tn-tj**2)/(t1 + tn - 2*tj)
    
    """
    if (t0 > t1):
        t0 = 2*x[0] - x[1]
        print("using two order estimator")
    
    if (t0 > t1):
        t0 = t1
        print("using t1")
    """
    
    return t0

def weibull_scale_transform(data, N):
    x = np.log(data)
    y = np.log(-np.log(1 - median_rank(len(data), N)))
    return x, y

def weib_ll(t, loc, scale, shape):
    return np.sum(np.log(weib_pdf(t, loc, scale, shape)))

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

def try_t0(tfail, N):
    n = len(tfail)
    j = np.ceil(n * p(n) * n / N)
    k = np.ceil(n * p(N))
    
    t0 = (tfail.min() * tfail.max() - tfail[j-1:k]**2)/(tfail.min() + tfail.max() - 2 * tfail[j-1:k])

    ll = np.empty(len(t0))
    for i in range(len(t0)):
        x, y = weibull_scale_transform(tfail - t0[i], N)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        shape = slope
        scale = np.exp(-intercept/slope)
        ll[i] = weib_ll(tfail, t0[i], scale, shape)
    print(t0, ll)
    return t0[ll.argmax()]
    

@route("/fitting", method='POST')
def fitting():
    #tfail = np.loadtxt("Fail_data.csv")
    if request.query.upload == "1":
        input_data = request.files.inputfile.file
    else:
        input_data = io.StringIO(request.forms.get("inputdata"))

    N = int(request.forms.get("lengthdata"))
    tfail = np.loadtxt(input_data)
    tfail.sort()
    x1, y1 = weibull_scale_transform(tfail, N)
    #t0 = t0_hat(tfail, N)
    t0 = try_t0(tfail, N)
    x2, y2 = weibull_scale_transform(tfail - t0, N)
    
    output1 = io.BytesIO()
    output2 = io.BytesIO()
    output3 = io.BytesIO()
    output4 = io.BytesIO()
    
    shape1, scale1, r_value1 = plot_linreg(x1, y1, output1, draw_line=False)
    #print ("Reliability: {}".format (reliability(tfail, 0, scale1, shape1)))
    shape2, scale2, r_value2 = plot_linreg(x2, y2, output2, draw_line=True)
    plot_pdf(tfail, t0, scale2, shape2, output3) #pdf of distribution fitted with location
    plot_pdf(tfail, 0, scale1, shape1, output4) #pdf of dist fitted without location
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
                R^2 (1) = {2} <br>
               
                R^2 (2) = {7} <br>
                Location Parameter = {5} <br>
                Shape Parameter = {8} <br>
                Scale Parameter = {9} <br>
                
                Log-Likelihood (1) = {10} <br>
                Log-Likelihood (2) = {11} <br>                
                
                Reliability: <input id ="reliability" name="reliability" type='text' />
                <input value="Find Reliable Life" id= "hitung_reliablelife" type='submit' />
                <input id="shape" name="shape" value="{8}" type='hidden' />
                <input  id="scale" name="scale" value="{9}" type='hidden' />
                <input  id="loc" name="loc" value="{5}" type='hidden' />
                <br>
                Reliable Life: <input  id="tfail" name="tfail" type='text' />
                <input value="Find Reliability" type='submit' id="hitung_reliability" />
            </td>
        </tr>
    </table>
    
     
    <script type="text/javascript" src="/static/js/jquery.min.js"></script>
    <script type="text/javascript" src="/static/js/scripts.js"></script>
    </body>
    </html>""".format(base64.encodebytes(output1.getvalue()).decode(),
            base64.encodebytes(output2.getvalue()).decode(),
            (r_value1**2),
            shape1,
            scale1,
            t0,
            base64.encodebytes(output3.getvalue()).decode(),
            (r_value2**2),
            shape2,
            scale2,
            weib_ll(tfail, 0, scale1, shape1),
            weib_ll(tfail, t0, scale2, shape2),
            base64.encodebytes(output4.getvalue()).decode())
    output1.close()
    output2.close()
    output3.close()
    output4.close()
    return html


@route("/")
def index():
    return template('template')

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

"""
<img src="data:image/png;base64,{1}"/>
<img src="data:image/png;base64,{12}"/>
 Shape Parameter1 = {3} <br>
 Scale Parameter1= {4} <br>
"""

import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/views/')) 

application=default_app()

#test_calc()
#run(host ='localhost', port=8080, debug=False)
