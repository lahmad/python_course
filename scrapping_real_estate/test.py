from  bs4 import BeautifulSoup


content = ''' <div _ngcontent-sc34="" class="left-content flex-one">
 <h3 _ngcontent-sc34="" class="price">
  <span _ngcontent-sc34="">
  </span>
  $615,900
  <app-listing-price-arrow _ngcontent-sc34="" _nghost-sc46="">
   <!-- -->
  </app-listing-price-arrow>
 </h3>
 <!-- -->
 <p _ngcontent-sc34="" class="address ng-star-inserted">
  <app-listing-address _ngcontent-sc34="" _nghost-sc47="">
   <!-- -->
   <span _ngcontent-sc47="" class="ng-star-inserted">
    <!-- -->
    <span _ngcontent-sc47="" class="ng-star-inserted">
     3560 CROSSWINDS Way,
    </span>
   </span>
   <span _ngcontent-sc47="" class="ng-star-inserted">
    <!-- -->
    <span _ngcontent-sc47="" class="ng-star-inserted">
     Ottawa,
    </span>
   </span>
   <span _ngcontent-sc47="" class="ng-star-inserted">
    <!-- -->
    <span _ngcontent-sc47="" class="ng-star-inserted">
     ON,
    </span>
   </span>
   <span _ngcontent-sc47="" class="ng-star-inserted">
    <!-- -->
    <span _ngcontent-sc47="" class="ng-star-inserted">
     K0A 2W0
    </span>
   </span>
  </app-listing-address>
 </p>
</div>
'''

soup = BeautifulSoup(content, 'html.parser')
h3content = soup.find('h3')
print ('Price', h3content.text.strip())

address = soup.find_all('span', 'ng-star-inserted')

address_set = set()

for item in address:
    element = str(item.text.strip())
    if len(element) > 0:
        address_set.add(element)

for item in address_set:
    print(item)
