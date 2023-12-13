#use selenium and start web browser firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

items_info = []

driver = webdriver.Firefox()

def clear_json():
    with open("items.json", "w") as json_file:
        json_file.write("")

def repair_json():
    with open("items.json", "r") as json_file:
        json_string = json_file.read()

    without_brackets = json_string.replace("[", "").replace("]", "")
    final_json_string = "[\n" + without_brackets + "\n]"

    with open("items.json", "w") as json_file:
        json_file.write(final_json_string)

def item_info(first_page=False):
        if first_page == True:
            item_list = driver.find_element(By.XPATH, "/html/body/div[1]/form/main/div/div[2]/div[1]/div[3]/div[1]/div[2]")
        else:
            item_list = driver.find_element(By.XPATH, "/html/body/div[1]/form/main/div/div[2]/div[1]/div[3]/div[1]/div")

        items = item_list.find_elements(By.TAG_NAME, "article")
        for item in items:
            item_link = item.find_element(By.CLASS_NAME, "mlc-itembox").get_attribute("href")
            item_name = item.find_element(By.TAG_NAME, "h3").text
            item_price = item.find_element(By.CLASS_NAME, "ml-offer-price__dollars").text
            end_time_element = item.find_element(By.XPATH, ".//span[@data-mlc-itembox-bidding-remaining-time]")
            item_timeleft = end_time_element.get_attribute('data-mlc-itembox-bidding-remaining-time')
            # .replace('"', '\\"')

            items_info.append({
                "name": item_name,
                "href": item_link,
                "price": item_price,
                "endTime": item_timeleft
            })

def main():
    clear_json()
    site = input("Wklej link: ")
    #site = "https://allegrolokalnie.pl/oferty/moda/uzywane?typ=licytacja"
    if 'https://allegrolokalnie.pl/' not in site:
        print("Nieprawidłowy link, to nie allegro lokalnie")
        main()
    elif '?typ=licytacja' not in site:
        print("Nieprawidłowy link, to nie licytacja")
        main()
    else:
        driver.get(site)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/button[1]").click()
        site_number = 1
        item_info(True)
        while True:
            try:
                time.sleep(0.5)
                site_number += 1
                driver.get(site + "&page=" + str(site_number))
                item_info()
            except:
                print("Koniec")
                with open("items.json", "a") as json_file:
                    json.dump(items_info, json_file, indent=2)
                # repair_json()
                break

main()



            # <article class="mlc-itembox__container is-desktop-vertical   " itemscope="" itemtype="http://schema.org/Offer">

#   <a data-card-analytics-click="0dbf5b8c-330d-41ca-bfc2-f2fe0b97d1fc" href="/oferta/zegarek-meski-invicta-subaqua-noma-iii" itemprop="url" class="mlc-card mlc-itembox" target="" rel="noopener noreferrer">
#     <div class="mlc-itembox__image">
#       <div class="mlc-itembox__image__wrapper">
#         <img src="https://a.allegroimg.com/s360x360/1e1ae0/715e064f41c49d80bf7e49ded35c" alt="Zegarek męski Invicta Subaqua Noma III" itemprop="image">

#       </div>
#     </div>
#     <div class="mlc-itembox__offer-container">
#       <div class="mlc-itembox__body-header">
#         <h3 class="mlc-itembox__title" itemprop="itemOffered">Zegarek męski Invicta Subaqua Noma III</h3>
#       </div>

#       <div class="mlc-itembox__following" data-mlc-follow-button-controller="{&quot;initialValue&quot;:false,&quot;offerId&quot;:&quot;0dbf5b8c-330d-41ca-bfc2-f2fe0b97d1fc&quot;,&quot;variant&quot;:&quot;with-text&quot;}"><label class="mlc-follow-button mlc-follow-button--with-text"><input type="checkbox" id="inputId" hidden="" data-testid="following-button"><span class="mlc-follow-button__text">Obserwuj</span><span class="ml-icon mlc-follow-button__icon ml-icon--green"><svg viewBox="0 0 24 24" focusable="false" aria-hidden="true"><use href="/images/ml-icons/icons.svg#heart-empty"></use></svg></span></label></div>

#       <div class="mlc-itembox__offer-info-container">

#         <ul class="mlc-itembox__params" itemprop="description">

#           <li class="mlc-itembox__params__param">
# <div class="ml-text-small">


# Waga produktu z opakowaniem jednostkowym: <span class="mlc-itembox__params__param__name"> 1 kg</span>


# </div>
#           </li>

#           <li class="mlc-itembox__params__param">
# <div class="ml-text-small">


# Płeć: <span class="mlc-itembox__params__param__name"> mężczyzna</span>


# </div>
#           </li>

#           <li class="mlc-itembox__params__param">
# <div class="ml-text-small">


# Marka: <span class="mlc-itembox__params__param__name"> Invicta</span>


# </div>
#           </li>

#           <li class="mlc-itembox__params__param">
# <div class="ml-text-small">


# Typ: <span class="mlc-itembox__params__param__name"> naręczny</span>


# </div>
#           </li>

#         </ul>

#         <div class="mlc-itembox__price-and-offer-badges-and-offer-type">
#           <div class="mlc-itembox__offer-attributes">



#           </div>
#           <span class="mlc-itembox__offer-type mlc-itembox__offer-type--bidding">Licytacja </span>

#           <div class="mlc-itembox__price">

# <span class="ml-offer-price ml-offer-price--size- mlc-itembox__price__offer-price">
#   <span class="ml-offer-price__dollars">299</span>


#   <span class="ml-offer-price__currency">&nbsp;zł</span>
# </span>

# <span class="mlc-smart-icon mlc-smart-icon--small mlc-itembox__smart-icon"><svg viewBox="0 0 74 20" fill="none" xmlns="http://www.w3.org/2000/svg">
# <g clip-path="url(#clip0_11459_204265)">
# <path d="M4.11708 15.1641C2.52753 15.1641 0 14.8061 0 13.3382C0 12.701 0.472569 12.2284 1.1313 12.2284C1.47499 12.2284 1.73991 12.3645 2.06212 12.522C2.54901 12.7654 3.15762 13.0733 4.382 13.0733C5.84267 13.0733 6.67325 12.6222 6.67325 11.8131C6.67325 9.74385 0.193324 11.1687 0.193324 6.96571C0.193324 4.70311 1.91892 3.30688 5.1553 3.30688C6.50856 3.30688 8.6566 3.55749 8.6566 4.99668C8.6566 5.64825 8.18403 6.1065 7.53246 6.1065C7.21026 6.1065 6.99545 5.9991 6.74485 5.86305C6.36536 5.66257 5.89279 5.41912 4.81877 5.41912C3.37958 5.41912 2.61345 5.84873 2.61345 6.63635C2.61345 8.99919 9.12917 7.30224 9.12917 11.5554C9.12201 13.732 7.29618 15.1641 4.11708 15.1641Z" fill="#422779"></path>
# <path d="M22.6976 15.164C22.0389 15.164 21.5091 14.6413 21.5091 13.9754V7.74613L18.2584 12.479C18.0149 12.8298 17.6139 13.0088 17.2488 13.0088C16.8836 13.0088 16.4826 12.8298 16.2392 12.479L12.9885 7.74613V13.9754C12.9885 14.6342 12.4658 15.164 11.7999 15.164C11.1412 15.164 10.6113 14.6413 10.6113 13.9754V4.48827C10.6113 3.88681 11.0409 3.29968 11.8644 3.29968C12.4443 3.29968 12.9169 3.58609 13.2391 4.05866L17.2846 9.94429L21.2871 4.05866C21.6093 3.58609 22.0461 3.29968 22.6189 3.29968C23.4423 3.29968 23.8719 3.87965 23.8719 4.48827V13.9754C23.8862 14.6342 23.3635 15.164 22.6976 15.164Z" fill="#422779"></path>
# <path d="M26.156 15.164C25.4758 15.164 24.7597 14.4552 25.1535 13.6103L29.6716 3.95842C29.8792 3.51449 30.3446 3.29968 30.8029 3.29968C31.2683 3.29968 31.7266 3.51449 31.9342 3.95842L36.395 13.4814C36.7959 14.3335 36.1157 15.1569 35.3138 15.1569C34.8699 15.1569 34.4474 14.9206 34.2469 14.4838L33.2302 12.3143H28.1894L27.1512 14.5411C26.9579 14.9492 26.5641 15.164 26.156 15.164ZM32.3566 10.3166L30.7098 6.77235L29.063 10.3166H32.3566Z" fill="#422779"></path>
# <path d="M38.8365 15.164C38.1778 15.164 37.6479 14.6413 37.6479 13.9754V4.65294C37.6479 3.99421 38.1706 3.46436 38.8365 3.46436L43.0682 3.47152C45.8177 3.47868 47.4215 4.92502 47.4215 7.27355C47.4215 8.99914 46.4907 10.245 45.0444 10.8178L46.8988 13.2451C47.0707 13.4671 47.1495 13.7177 47.1423 13.9898C47.1423 14.6843 46.6626 15.1712 45.9537 15.1497C45.5742 15.1425 45.2449 14.9922 45.0157 14.6843L42.3307 11.1687H40.0251V13.9611C40.018 14.6342 39.4953 15.164 38.8365 15.164ZM42.839 9.1495C44.2854 9.1495 45.0444 8.55521 45.0444 7.41675C45.0444 6.27829 44.2782 5.684 42.839 5.684H40.018V9.1495H42.839Z" fill="#422779"></path>
# <path d="M52.0398 5.76988H49.1471C48.5098 5.76988 48.0015 5.26151 48.0015 4.62426C48.0015 3.98701 48.5098 3.47864 49.1471 3.47864H57.3096C57.9469 3.47864 58.4553 3.98701 58.4553 4.62426C58.4553 5.26151 57.9469 5.76988 57.3096 5.76988H54.4169V13.9682C54.4169 14.627 53.8943 15.1568 53.2284 15.1568C52.5625 15.1568 52.0398 14.6341 52.0398 13.9682V5.76988Z" fill="#422779"></path>
# <path d="M68.1974 9.98004L65.4622 9.95856L64.2378 3.271L69.5148 3.3068L68.1974 9.98004Z" style="fill: white !important"></path>
# <path d="M68.1973 9.98009L65.4622 9.95861L64.2378 3.27105L69.5148 3.30685L68.1973 9.98009ZM66.7939 15.2142C65.7342 15.2142 64.8822 14.3549 64.8822 13.2952C64.8822 12.2355 65.7414 11.3835 66.8011 11.3835C67.8608 11.3835 68.7129 12.2427 68.7129 13.3024C68.7129 13.3096 68.7129 13.3167 68.7129 13.3167C68.7057 14.3693 67.8465 15.2142 66.7939 15.2142ZM66.8369 0.449951C62.8702 0.485752 59.6696 3.71497 59.6768 7.68169C59.6768 12.9014 66.8369 19.5174 66.8369 19.5174C67.2522 19.1451 73.997 12.9301 73.997 7.68169C74.0042 3.71497 70.8036 0.478592 66.8369 0.449951Z" fill="#FF5A00"></path>
# <path d="M66.7938 15.207C65.7341 15.207 64.8821 14.3406 64.8821 13.2881C64.8821 12.2284 65.7485 11.3763 66.801 11.3763C67.8607 11.3763 68.7128 12.2427 68.7128 13.2953C68.7128 13.3024 68.7128 13.3024 68.7128 13.3096C68.7056 14.3693 67.8464 15.2142 66.7938 15.207Z" style="fill: white !important"></path>
# </g>
# <defs>
# <clipPath id="clip0_11459_204265">
# <rect width="74" height="20" fill="white"></rect>
# </clipPath>
# </defs>
# </svg>
# </span>

#           </div>

#           <div class="mlc-itembox__bidding-props">
#             <span class="mlc-itembox__bidding-props__prop">
#               <span class="ml-icon ml-icon--small mlc-itembox__bidding-props__prop__icon">
# <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
# <path d="M17.618 5.968L19.071 4.515L20.485 5.929L19.032 7.382C20.4678 9.17917 21.1609 11.4579 20.9691 13.7501C20.7772 16.0424 19.715 18.1742 18.0005 19.7077C16.286 21.2412 14.0494 22.0601 11.75 21.9961C9.4506 21.9321 7.26301 20.9901 5.63647 19.3635C4.00993 17.737 3.06793 15.5494 3.00392 13.25C2.93991 10.9506 3.75875 8.71402 5.29228 6.99951C6.82581 5.285 8.95761 4.22275 11.2499 4.03092C13.5421 3.83909 15.8208 4.53223 17.618 5.968ZM12 20C12.9193 20 13.8295 19.8189 14.6788 19.4672C15.5281 19.1154 16.2997 18.5998 16.9497 17.9497C17.5998 17.2997 18.1154 16.5281 18.4672 15.6788C18.8189 14.8295 19 13.9193 19 13C19 12.0807 18.8189 11.1705 18.4672 10.3212C18.1154 9.47194 17.5998 8.70026 16.9497 8.05025C16.2997 7.40024 15.5281 6.88463 14.6788 6.53284C13.8295 6.18106 12.9193 6 12 6C10.1435 6 8.36301 6.7375 7.05025 8.05025C5.7375 9.36301 5 11.1435 5 13C5 14.8565 5.7375 16.637 7.05025 17.9497C8.36301 19.2625 10.1435 20 12 20ZM11 8H13V14H11V8ZM8 1H16V3H8V1Z" fill="#767676"></path>
# </svg>

#               </span>
#               <span data-mlc-itembox-bidding-remaining-time="{&quot;endingAt&quot;:&quot;2023-12-16T11:29:50.829661Z&quot;}">06:13:17 do końca</span>
#             </span>
#             <span class="mlc-itembox__bidding-props__prop">
#               <span class="ml-icon ml-icon--small mlc-itembox__bidding-props__prop__icon">
# <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
# <path d="M14 20V22H2V20H14ZM14.586 0.686005L22.364 8.464L20.95 9.88L19.89 9.526L17.413 12L23.07 17.657L21.656 19.071L16 13.414L13.596 15.818L13.879 16.95L12.464 18.364L4.686 10.586L6.101 9.172L7.231 9.45401L13.525 3.161L13.172 2.101L14.586 0.686005ZM15.293 4.222L8.222 11.292L11.757 14.828L18.828 7.758L15.293 4.222Z" fill="#767676"></path>
# </svg>

#               </span>
# 0 osób licytuje
#             </span>
#           </div>

#         </div>
#       </div>

#       <div class="mlc-itembox__badges">


#   <ul class="ml-badges ml-badges mlc-itembox__badges__badge">

#       <li data-for="" data-tip="" class="ml-badges__badge ">
#             <svg class="ml-badges__badge-image">
#                 <use href="/images/badges/badges-metrum.svg#c2c"></use>
#             </svg>
# Osoba prywatna
#       </li>

#   </ul>
# <div id="ml-badges-tooltips" data-tooltip-id="{&quot;tooltipId&quot;:null}"></div>


#       </div>


#       <div class="mlc-itembox__location" itemprop="areaServed" itemscope="" itemtype="http://schema.org/Place">
#         <address itemprop="address">Łódź, Bałuty</address>
#       </div>
#     </div>
#   </a>


# </article>