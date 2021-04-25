Feature: checking products

  Scenario: add a product
    Given we want to add a product
    When we fill in the form
    Then it succeeds
  
  Scenario: adding products
    Given we have specific products to add
    | name          | price  | image_url     | brand  |
    | this one      | 23.45  | https://st4.depositphotos.com/1067336/37766/i/600/depositphotos_377665796-stock-photo-belgorod-russia-may-2020-classic.jpg | nike   | 
    | another thing | 34.56  | https://st4.depositphotos.com/1067336/37766/i/600/depositphotos_377665796-stock-photo-belgorod-russia-may-2020-classic.jpg | adidas |
    When we visit the listing page
    Then we will find 'another thing'
    
 