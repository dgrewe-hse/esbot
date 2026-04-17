Feature: User management

  Scenario: Ask a Question
    Given the API is running
    When I send a POST request to "api/v1/message" with valid data
    Then the response status should be 201