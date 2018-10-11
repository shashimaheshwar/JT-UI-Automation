# a=[3,2,11,5,4,3,2,3,2,32]
# b=[13,4,11,4,5,11,9]
# c=[]
# len_of_c=len(a)+len(b)
# for i in range(0,len_of_c):
#     try:
#         a_m=0 if len(a) < 1 else max(a)
#         b_m = 0 if len(b) < 1 else max(b)
#
#         if  a_m > b_m:
#             c.append(a_m)
#             a.remove(a_m)
#         else:
#             c.append(b_m)
#             b.remove(b_m)
#     except:
#         print("List Empty")
# c.reverse()
# print(c)


# from selenium import webdriver
# import time
# driver = webdriver.Chrome()
# driver.maximize_window()
# driver.get('https://vbo-staging.justickets.co/?utf8=%E2%9C%93&date=&tags%5B%5D=86d3c756-2289-4c9c-99e4-437fcde075fd')
# time.sleep(70)
# elemenlists= driver.find_elements_by_xpath("//*//a[contains(text(),'Cancel')]")
# for element in elemenlists:
#     element.click()
#     time.sleep(2)
#     #driver.find_element_by_id('cancellation_reason').click()
#     #time.sleep(1)
#     driver.find_element_by_xpath('//*[@id="cancellation_reason"]/option[4]').click()
#     time.sleep(1)
#     driver.find_element_by_id('cp').send_keys('justickets')
#     driver.find_element_by_xpath("//*[@type = 'submit']").click()
#     time.sleep(5)
