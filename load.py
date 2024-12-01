import whisper

def load_model(model_name="base"):
    model = whisper.load_model(model_name)


if __name__ == "__main__":
    load_model()
