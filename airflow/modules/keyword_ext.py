from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, size, explode, monotonically_increasing_id
from pyspark.sql.types import ArrayType, StringType
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer as CountVectorizer_sklearn
from sentence_transformers import SentenceTransformer
from bareunpy import Tagger
import datetime
import os
import subprocess
from pyarrow import fs

# Spark 세션 초기화
spark = SparkSession.builder \
    .appName("KeywordExtraction") \
    .getOrCreate()

# 모델 초기화
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
model_broadcast = spark.sparkContext.broadcast(model)



# Tagger를 초기화하는 함수
def keyword_ext(texts):
    tagger = Tagger('koba-Q2CYNCI-XZ7E7PI-X6YRKPY-K4Z2KMY')
    model = model_broadcast.value
    results = []
   
    for text in texts:
        if text is None or not text.strip():
            results.append([])
            continue

        tokenized_doc = tagger.pos(text)  # phrase 인수로 text를 전달
        tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'NNG' or word[1] == 'NNP'])
        if not tokenized_nouns.strip():
            results.append([])
            continue

        try:
            count = CountVectorizer_sklearn(ngram_range=(1, 1)).fit([tokenized_nouns])
            candidates = count.fit([tokenized_nouns]).get_feature_names_out()
        except ValueError as e:
            if str(e) == 'empty vocabulary; perhaps the documents only contain stop words':
                results.append([])
                continue
            else:
                raise
        if len(candidates) == 0:
            results.append([])
            continue

        doc_embedding = model.encode([text])
        candidate_embeddings = model.encode(candidates)

        keywords = mmr(doc_embedding, candidate_embeddings, candidates, top_n=5, diversity=0.2)
        results.append(keywords)

    return results

def mmr(doc_embedding, candidate_embeddings, words, top_n, diversity):
    """다양성을 고려한 최대 마진 적중률(MMR)을 계산하여 키워드를 추출합니다."""
    word_doc_similarity = cosine_similarity(candidate_embeddings, doc_embedding)
    word_similarity = cosine_similarity(candidate_embeddings)

    if len(word_doc_similarity) == 0 or len(word_similarity) == 0:
        return []

    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)
        mmr = (1 - diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)

        if mmr.size == 0:
            break

        mmr_idx = candidates_idx[np.argmax(mmr)]
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [words[idx] for idx in keywords_idx]


# hadoop 설정 초기화
# file_path = f"/test/2024-07-01_small.csv"
classpath = subprocess.Popen(["/home/ksk/hadoop/bin/hdfs", "classpath", "--glob"], stdout=subprocess.PIPE).communicate()[0]
os.environ["CLASSPATH"] = classpath.decode("utf-8")
hdfs = fs.HadoopFileSystem(host='192.168.0.206', port=8020, user='ksk')

# 뉴스 내용을 포함한 CSV 파일 읽기
# 경로 hdfs로 재설정 해야함!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
today = datetime.datetime.today().strftime("%Y-%m-%d")
news_contents_df = spark.read.csv("hdfs:/test/2024-07-01_small.csv", header=True, inferSchema=True, encoding="utf-8")

# keyword_ext UDF 적용하여 키워드 추출
news_rdd = news_contents_df.select("content").rdd.map(lambda row: row[0])
keywords_rdd = news_rdd.mapPartitions(keyword_ext)
keywords_df = keywords_rdd.zipWithIndex().toDF(["Keywords", "Index"])

# 원본 데이터프레임과 조인
news_contents_df = news_contents_df.withColumn("Index", monotonically_increasing_id())
news_contents_df = news_contents_df.join(keywords_df, on="Index").drop("Index")

# Keywords가 비어 있는 행은 필터링합니다.
news_contents_df = news_contents_df.filter(size(col("Keywords")) > 0)

# CountVectorizer를 사용하여 키워드 빈도 계산 준비
keywords_exploded = news_contents_df.withColumn("Keyword", explode(col("Keywords")))
keyword_counts = keywords_exploded.groupBy("Keyword").count().withColumnRenamed("count", "Count")

# 결과를 CSV 파일로 저장
# 경로 hdfs로 재설정 해야함!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
keyword_counts.write.csv(f"hdfs:/test/2024-07-01_small_keyword_counts.csv", header=True, encoding='utf-8-sig')

# Spark 세션 종료
spark.stop()
