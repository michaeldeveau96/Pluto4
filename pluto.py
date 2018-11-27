import random
import time
import matplotlib.pyplot as plt
import nmap
import pyspeedtest


class GetData:

    def __init__(self):
        self.devices = []
        self.average_ping = ''
        self.average_download = ''
        self.average_upload = ''

    def get_devices(self):
        nm = nmap.PortScanner()
        print('Gathering Devices...')
        print('----------------------------------------------------')
        start = time.time()
        nm.scan(hosts='192.168.0.1/24', arguments='-n -sP')
        self.devices = nm.all_hosts()
        end = time.time()
        ptime = end-start
        print('Gathered Devices. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.devices

    def get_average_ping(self):
        st = pyspeedtest.SpeedTest()
        print('Calculating average ping...')
        print('----------------------------------------------------')
        start = time.time()
        pings = []
        for i in range(0, len(self.devices)):
            pings.append(st.ping())
        self.average_ping = round(sum(pings)/len(pings))
        end = time.time()
        ptime = end-start
        print('Calculated average ping. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_ping

    def get_average_download(self):
        st = pyspeedtest.SpeedTest()
        print('Calculating average download...')
        print('----------------------------------------------------')
        start = time.time()
        downloads = []
        for i in range(0, len(self.devices)):
            downloads.append(st.download()/1000000)
        self.average_download = round(sum(downloads)/len(downloads))
        end = time.time()
        ptime = end - start
        print('Calculated average download. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_download

    def get_average_upload(self):
        st = pyspeedtest.SpeedTest()
        print('Calculating average upload...')
        print('----------------------------------------------------')
        start = time.time()
        uploads = []
        for i in range(0, len(self.devices)):
            uploads.append(st.upload()/1000000)
        self.average_upload = round(sum(uploads)/len(uploads))
        end = time.time()
        ptime = end - start
        print('Calculated average upload. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_upload

    def plot(self):
        st = pyspeedtest.SpeedTest()
        print('Drawing network...')
        print('----------------------------------------------------')
        start = time.time()
        responses = []
        downloads = []
        uploads = []
        for ip in self.devices:
            ping = st.ping()
            download = st.download()
            upload = st.upload()
            if round(ping) > (int(self.average_ping)*1.5):
                responses.append('HIGH ' + str(round(ping)) + 'ms')
            else:
                responses.append('NORMAL ' + str(round(ping)) + 'ms')
            if round(download/1000000) < (int(self.average_download)*.75):
                downloads.append('LOW ' + str(round(download/1000000)) + 'Mbps')
            else:
                downloads.append('NORMAL ' + str(round(download/1000000)) + 'Mbps')
            if round(upload/1000000) < (int(self.average_upload)*.75):
                uploads.append('LOW ' + str(round(upload/1000000)) + 'Mbps')
            else:
                uploads.append('NORMAL ' + str(round(upload/1000000)) + 'Mbps')
        hostnames = []
        p = 1
        for ip in self.devices:
            if ip == '192.168.0.1':
                hostnames.append('Router')
            else:
                hostnames.append('Computer ' + str(p))
            p += 1
        x = []
        y = []
        for i in range(0, len(self.devices)):
            x.append(random.random())
            y.append(random.random())
        area = 20

        plt.scatter(x, y, s=area)
        plt.xticks([])
        plt.yticks([])

        plt.plot(x, y, linestyle='None', marker='o', markersize=5)

        for i, txt in enumerate(self.devices):
            if 'HIGH' in responses[i]:
                txt = 'Device Name: ' + str(hostnames[i]) + '\n' + \
                      'Device IP: ' + str(self.devices[i]) + '\n' + \
                      'Ping: ' + str(responses[i]) + '\n' + \
                      'Download: ' + str(downloads[i]) + '\n' + \
                      'Upload: ' + str(uploads[i])
                plt.annotate(txt, (x[i], y[i]), color='red')
            elif 'LOW' in downloads[i]:
                txt = 'Device Name: ' + str(hostnames[i]) + '\n' +\
                      'Device IP: ' + str(self.devices[i]) + '\n' + \
                      'Ping: ' + str(responses[i]) + '\n' + \
                      'Download: ' + str(downloads[i]) + '\n' + \
                      'Upload: ' + str(uploads[i])
                plt.annotate(txt, (x[i], y[i]), color='red')
            elif 'LOW' in uploads[i]:
                txt = 'Device Name: ' + str(hostnames[i]) + '\n' + \
                      'Device IP: ' + str(self.devices[i]) + '\n' + \
                      'Ping: ' + str(responses[i]) + '\n' + \
                      'Download: ' + str(downloads[i]) + '\n' + \
                      'Upload: ' + str(uploads[i])
                plt.annotate(txt, (x[i], y[i]), color='red')
            else:
                txt = 'Device Name: ' + str(hostnames[i]) + '\n' + \
                      'Device IP: ' + str(self.devices[i]) + '\n' + \
                      'Ping: ' + str(responses[i]) + '\n' + \
                      'Download: ' + str(downloads[i]) + '\n' + \
                      'Upload: ' + str(uploads[i])
                plt.annotate(txt, (x[i], y[i]), color='green')
        end = time.time()
        ptime = end - start
        print('Calculated average upload. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return plt.show()

def main():

    print('Scanning your network...')
    data = GetData()
    data.get_devices()
    data.get_average_ping()
    data.get_average_download()
    data.get_average_upload()
    data.plot()

if __name__ == '__main__':
    main()