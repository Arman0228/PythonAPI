def test_phrase_length():
    phrase = input("Set a phrase (shorter than 15 characters): ")
    assert len(phrase) < 15, "Phrase length is 15 or more characters"