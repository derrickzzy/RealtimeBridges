import os
import shutil
import imp
from server.models import Bridge
import datetime
from numpy import genfromtxt,zeros,load,save
import numpy as np
from scipy.stats import ranksums
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
from server.call import call
import requests
from django.template.loader import render_to_string

def processevent(bridgenumber,directory):
    tempdir = directory + '/temp/'
    file_names = os.listdir(tempdir)
    datadir = directory + '/data.csv'        # directiro for gdf
    for filename in file_names:
        tempdata = open(tempdir + filename, 'rb')
        data = open(datadir, 'a+')
        data.write('\n')
        while 1:
            data_line = tempdata.readline()
            data.write(data_line)
            if not data_line:
                break
        data.close()
        tempdata.close()
        os.remove(tempdir + filename)
        print "removed temp file -------------------------"
        with open(datadir) as myfile:
            count = sum(1 for line in myfile)
        print "count number of events -------------------------"
        print count
        if count >= 500:
            DI = round(damageindex(datadir),2)
            print "DI analysis complete -------------------------"
            foo = bridgesignature(bridgenumber,directory,datadir)
            print "signature analysis complete -------------------------"
            obj = Bridge.objects.get(number=bridgenumber)
           
            
            if DI <= 0.16:
                obj.conditions = 'g'
            else:
                if DI < 0.5:
                    msg_condition = "Yellow"
                    obj.conditions = 'y'
                else:
                    obj.conditions = 'r'
                    msg_condition = "Red"
                    #make alert call
                    #call()
                    print 'make call complete----------------------------'
                """
                # Make PDF
                time = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
                import MakePDF
                MakePDF.pdf(obj,msg_condition, DI)
                """
                # send email
                send_simple_message(obj,msg_condition,DI)
                
                obj.save()

# function to calculate damage index
def damageindex(datadir):
    # define significant level
    alpha = 0.05
    damagedgirder = 0
    print datadir
    print "DI Function called -------------------------"
    # load GDFs and temperature
    data = np.genfromtxt(datadir, delimiter=',')
    print data.shape
    # get GDFs
    gdf = data[:,:]
    # define recent sample set
    samplegdf = gdf[-50:,:]
    # get total number of girders
    totalgirder = gdf.shape[1]
    print "obtained gdfs -------------------------"
    # for each girder, perform ranksum test
    print gdf.shape[1]
    for girder in range(0,gdf.shape[1]):
        (ttest,pvalue) = ranksums(gdf[:,girder], samplegdf[:,girder])
        # if significantly different
        print pvalue
        if pvalue < alpha:
            damagedgirder +=1.0
    # compute DI value
    print damagedgirder
    print totalgirder
    DI = damagedgirder/totalgirder
    print DI

    # returen the results
    return (DI)

def bridgesignature(bridgenumber,directory,datadir):
    # load GDFs and temperature
    data = np.genfromtxt(datadir, delimiter=',')
    # get GDFs
    gdf = data[:, :]
    # define sample size for signature
    signature_size = 50
    # obtain total number of events and total number of girder
    (totalrecord,totalgirder) = gdf.shape

    # check if baseline bridge signature has been created.
    signaturedir = directory+'/signature.npy' 
    if not os.path.exists(signaturedir):       # if it doesn't exist
        print "signature file doesn't exist -------------------------"
        # initiate the matrix
        signature_low = np.zeros((signature_size,totalgirder))
        signature_high = np.zeros((signature_size,totalgirder))
        sampleset = np.zeros((signature_size,totalgirder,1000))
        gdf_low = np.zeros((1,totalgirder))
        gdf_high = np.zeros((1,totalgirder))
        test = open('test.txt', 'a+')
        test.write('sig2 is done')
        test.close()
        # for each gider
        for girder in range(0, totalgirder):
            for rank in range(0,signature_size ):
                for sample in range(0,999):
                    sampleset[rank,girder,sample] = sorted(gdf[random.sample(range(0,totalrecord-1),signature_size),girder])[rank]
                sampleset[rank,girder,:] = sorted(sampleset[rank,girder,:])
                signature_low[rank, girder] = sampleset[rank,girder,:][25]
                signature_high[rank, girder] = sampleset[rank,girder,:][975]
        # save signature
        signature = (signature_low,signature_high)
        np.save(signaturedir,signature)
    # the signature file already exist
    else:
        print "signature file does exist -------------------------"
        signature = np.load(signaturedir)
        signature_low = signature[0]
        signature_high = signature[1]
 
    # construct the plot for girder envelope
    signature_recent = gdf[-signature_size:,:]
    P_rank = range(1,signature_size+1 )
    P_rank[:] = [float(x) / signature_size for x in P_rank]
    print "get variables -------------------------"
    for girder in range(0, totalgirder):
        print girder
        titlestr = 'Girder '+ str(girder+1) + ' Signature'
        pltdir = 'RealtimeBridge/static/'+ str(bridgenumber)+ '/Girder'+str(girder+1) + 'Signature.png'
        plt.plot(P_rank,signature_low[:,girder],'#28B463')
        plt.plot(P_rank,signature_high[:,girder],'#28B463',label='95% Tolerance Envelope')
        plt.plot(P_rank,sorted(signature_recent[:,girder]),'#FF7D33',label='Girder Signature')
        plt.xlabel('Probability of Exceedance')
        plt.ylabel('Girder Distribution Factor')
        plt.title(titlestr)
        plt.grid(True)
        legend = plt.legend(loc='upper center', shadow=True, fontsize='x-large')
        if os.path.exists(pltdir):
            try:
                os.remove(pltdir)
            except OSError as e:
                test = open('test.txt', 'a+')
                test.write('error/:%s ' % e.strerror )
                test.close()
        plt.savefig(pltdir)
        test = open('test.txt', 'a+')
        test.write('saved')
        test.close()
        plt.close()
    print "girder envelop complete -------------------------"

    # construct the plot for bridge signature
    y =np.arange(1, totalgirder+1, 1)
    X, Y = np.meshgrid(P_rank, y)
    Z_low = np.transpose(signature_low)
    Z_high = np.transpose(signature_high)
    Z_recent =np.transpose(signature_recent)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf_low = ax.plot_surface(X, Y, Z_low,rstride=1, cstride=1,
                           linewidth=0, antialiased=False,color='#28B463')
    surf_low = ax.plot_surface(X, Y, Z_high,rstride=1, cstride=1,
                           linewidth=0, antialiased=False,color='#28B463')
    surf_signature = ax.plot_surface(X, Y, Z_recent,rstride=1, cstride=1,
                           linewidth=0, antialiased=False,color='#FF7D33')
    
    ax.set_zlim3d(0, 0.4)
    ax.view_init(elev=25., azim=-10)
    ax.set_xlabel('Probability of Exceedance')
    ax.set_ylabel('Girders')
    ax.set_zlabel('Girder Distribution Factor')
    titlestr = 'Bridge Signature'
    pltdir = 'RealtimeBridge/static/'+ str(bridgenumber)+ '/BridgeSignature.png'
    #if os.path.exists(pltdir):
    #    os.remove(pltdir)
    plt.savefig(pltdir)
    plt.close()

    return 0

def send_simple_message(obj,msg_condition,DI):
    rendered = render_to_string('email.html', {'bnum': obj.number,'bloc':obj.town+', '+obj.state, 'bcondition':msg_condition,'bDI':DI,'bpk':obj.pk })
    return requests.post(
        "https://api.mailgun.net/v3/sandbox2abc6eaeb72a4c12876535d6fdb20703.mailgun.org/messages",
        auth=("api", "key-5c74fcc384b1b7f01bcc94f28fd107b6"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox2abc6eaeb72a4c12876535d6fdb20703.mailgun.org>",
              "to": "derrickzhao <zhiyong.zhao@tufts.edu>",
              "subject": "Real-time Bridge Monitoring Alert",
              "html":rendered})
