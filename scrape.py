def scrape():
    from bs4 import BeautifulSoup as bs
    from splinter import Browser
    import requests
    import pandas as pd
    import pymongo
    import time 
    
    mars_dict = {}
# NASA Mars News to scrape News Title and Paragraph Text     
    # URL of NASA Mars News Site webpage to be scraped
    url = 'https://mars.nasa.gov/news'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    #print(soup.prettify())
    
    
    news_title = soup.title.text
    #print(title)
    mars_dict["News title"] = news_title
    
    news_paragraph = soup.find("div", class_="rollover_description_inner").text
    #print(news_paragraph)
    mars_dict["News Paragraph"] = news_paragraph
    
# JPL Mars Space Images - Use SPlinter to find the full size image url
     #pointing to the directory where chromedriver exists
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser("chrome", **executable_path, headless = True)    
     
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
     
     # image url to full size of the image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup2 = bs(html, 'html.parser')
    #print(soup2)
    
    #image_url = soup.find('img', class_='fancybox-image')['src']
    image_url = soup2.find('figure', class_='lede')
    image_link = image_url.a["href"]
    featured_image_url='https://www.jpl.nasa.gov/' + image_link
    #print(featured_image_url)
    
    mars_dict["Featured image url"] = featured_image_url
    
    #scrape the latest Mars weather tweet from the page.
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    #print(soup)
    
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(mars_weather)
    
# # Mars Facts using Pandas-scrape the table containing planet facts Diameter, Mass, etc. 
    
    url = 'http://space-facts.com/mars/'
    marsfacts = pd.read_html(url)
    #marsfacts
    
    # Using .rename(columns={}) in order to rename columns
    marsfacts_df = marsfacts[0]
    renamed_marsfacts_df = marsfacts_df.rename(columns={0:"Facts", 1:"Value"})
    #renamed_marsfacts_df
    
    #mars_facts=mars_facts.set_index('description')
    renamed_marsfacts_df1 = renamed_marsfacts_df.set_index('Facts')
    #renamed_marsfacts_df1
    
    #Convert df to html table string
    marsfacts_html=renamed_marsfacts_df.to_html()
    #print(marsfacts_html)
    
# Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser').find_all("a",class_ = "itemLink product-item")
    hemi_titles = []
    for i in soup:
        title = i.find("h3").text
        link= i["href"]
        hemi_titles.append(title)
    #print(title,"",link)    
    
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser("chrome", **executable_path, headless = True)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    hemi_imglist = []
    for x in range(len(hemi_titles)):
        try:
            browser.click_link_by_partial_text(hemi_titles[x])
        except:
            browser.find_link_by_text('2').first.click()
            browser.click_link_by_partial_text(hemi_titles[x])
        html = browser.html
        soup2 = bs(html, 'html.parser')
        hemi_soup = soup2.find('div', 'downloads')
        hemi_url = hemi_soup.a['href']
        #urls.append(hemi_url)
    
        hemi_dict={"title": hemi_titles[x], 'img_url': hemi_url}
        hemi_imglist.append(hemi_dict)
        #print(hemi_imglist)
    mars_dict['Mars_Hemispheres_urls']=hemi_imglist

    return mars_dict    
     