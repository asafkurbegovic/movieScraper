from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')


def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

driver.get('https://www.rottentomatoes.com/search?search=the%20social%20network')
root= driver.find_element_by_tag_name('search-result-container')

# html_of_interest=driver.execute_script('return arguments[0].innerHTML',root)
# sel_soup = BeautifulSoup(html_of_interest,'html.parser')


shadowelEl = expand_shadow_element(root)

html_of_interest = driver.execute_script('return arguments[0].innerHTML',shadowelEl)
sel_soup = BeautifulSoup(html_of_interest,'html.parser')
root1=[]

root1 =  shadowelEl.find_elements_by_tag_name('search-result')

print(root1[1])
print('------------------------')
for x in range (len(root1)):
  shadowelEl1 = expand_shadow_element(root1[x])
  html_of_interest = driver.execute_script('return arguments[0].innerHTML', shadowelEl1)
  sel_soup = BeautifulSoup(html_of_interest, 'html.parser')
  print('<<<<<<<<<<<',x,'>>>>>>>>>>>>>>>>')
  print(sel_soup)











driver.close()