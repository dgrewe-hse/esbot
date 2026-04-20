Feature: Resume existing learning session Benni

Scenario: Student wants to resume session
    Given the API is running
    Given the database is seeded with messages
    When the student requests an old session with session-id
    Then the response should contain all messages with that session-id
    
Scenario: Student want to resume a session which does not exist
    Given the API is running
    When the student request an session with a unknown session-id
    Then the response status should be 404
    Then the response should contain "did not find your session"