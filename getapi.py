import requests,os
from urllib.request import urlretrieve

class getCarName():
    """
    author：alisa
    初始化部分，是公共变量
    """
    def __init__(self,appkey="你获取到的appkey",getNum=100):
        self.appkey = appkey
        self.getNum = getNum
        self.url = 'http://api.jisuapi.com/car/brand'
        self.loginUrl = 'https://www.jisuapi.com/my/login.php?act=login&rtype=json'
        self.password = "123456"
        self.mobile = "123456"


    def delete_file_folder(self,src):
        """

        :参数 src:
        :此函数作用是删除文件或者目录
        """
        if os.path.isfile(src):
            try:
                os.remove(src)
            except:
                pass
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc=os.path.join(src,item)
                self.delete_file_folder(itemsrc)
            try:
                os.rmdir(src)
            except:
                pass



    def login(self):
        """
        登录，获取登录状态码
        :return: 登录状态码
        """

        data = {"mobile":self.mobile,"password":self.password}
        respon = requests.post(self.loginUrl,data=data,stream=True)
        return respon.status_code


    def get_car_name(self,dirName):
        """

        :参数 目录名称:
        :返回: 汽车大全api中的汽车名片
        """

        self.delete_file_folder(dirName)
        os.mkdir(dirName)
        if self.login()==200:
            params = {}
            params['appkey'] = self.appkey

            resp = requests.get(self.url,params=params)
            if resp.json().get('status') == '0':
                carNumber = len(resp.json().get('result',None))

                num = self.getNum if self.getNum <= carNumber else carNumber

                for j,i in enumerate(resp.json().get("result",None)[0:num]):
                    print (i.get("logo",None))
                    res = requests.get(i.get("logo",None))
                    if res.status_code == 200:
                        with open('./{}/{}.png'.format(dirName,i.get("name",None)),'wb') as f:
                            f.write(res.content)
            else :
                print ("汽车大全请求失败")

        else:
            print ('login fail')


if __name__ == '__main__':
    carName = getCarName()
    carName.get_car_name(r'picturepict')
