from selenium import webdriver
from time import sleep
#from secrets import pw
from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from follow.models import loginarea
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException

# Create your views here

def login1(request):
    if request.method=='POST':
        rusername=request.POST['username']
        rpassword =request.POST['password']
        data = loginarea(username=rusername, password=rpassword)
        data.save()

        return follow1(request)
    return render(request,'follow/form.html')







def follow1(request):
    data1 = loginarea.objects.values_list('username')
    data2 = loginarea.objects.values_list('password')


    class InstaBot:
        def __init__(self, username, pw):


            self.driver = webdriver.Chrome()
            self.username = username
            #self.driver = webdriver.Chrome()
            #self.username = username
            self.driver.get("https://instagram.com")
            sleep(2)
            # self.driver.find_element_by_xpath("//a[contains(text(), 'Log In')]")\
            # .click()
            sleep(2)
            self.driver.find_element_by_xpath("//input[@name=\"username\"]") \
                .send_keys(username)

            self.driver.find_element_by_xpath("//input[@name=\"password\"]") \
                .send_keys(pw)
            self.driver.find_element_by_xpath('//button[@type="submit"]') \
                .click()
            sleep(10)
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
                .click()
            sleep(2)
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
                .click()
            sleep(2)

        def get_unfollowers(self):
            self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)) \
                .click()
            sleep(2)
            self.driver.find_element_by_xpath("//a[contains(@href,'/following')]") \
                .click()
            following = self._get_names()
            self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]") \
                .click()
            followers = self._get_names()
            # not_following_back = [user for user in following if user not in followers]
            # print(not_following_back)

            print(len(followers))
            print(len(following))
            answer = [user for user in following if user not in followers]
            return answer

        def _get_names(self):
            sleep(2)
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div")
            last_ht, ht = 0, 1
            while last_ht != ht:
                last_ht = ht
                sleep(1)
                ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                    return arguments[0].scrollHeight;
                    """, scroll_box)
            links = scroll_box.find_elements_by_tag_name('a')
            names = [name.text for name in links if name.text != '']
            # close button

            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button") \
                .click()
            return names

    p=InstaBot(data1[len(data1)-1][0],data2[len(data2)-1])
    bipin=p.get_unfollowers()
    l=len(bipin)
    return render(request,'follow/list.html',{'bipin':bipin[2:]})

