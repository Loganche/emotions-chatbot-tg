import chatbot
import sentiment
import emotion

m_chat, t_chat = chatbot.model_tokenizer()
chatbot.save_model_tokenizer(m_chat, t_chat, 'model_chat', 'tokenizer_chat')

m_sentiment, t_sentiment = sentiment.model_tokenizer()
sentiment.save_model_tokenizer(m_sentiment, t_sentiment, 'model_sentiment', 'tokenizer_sentiment')

# m_emotion, t_emotion = emotion.model_tokenizer()
# emotion.save_model_tokenizer(m_emotion, t_emotion, 'model_emotion', 'tokenizer_emotion')
