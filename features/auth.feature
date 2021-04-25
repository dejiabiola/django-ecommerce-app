Feature: checking auth

  Scenario: check login works
    Given we want to login a user
    When we fill in the login form with correct data
    Then it succeeds by navigating to product 
  
  
 