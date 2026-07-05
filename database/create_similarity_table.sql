DROP TABLE IF EXISTS similarity_result;

CREATE TABLE similarity_result
(
    id SERIAL PRIMARY KEY,

    analysis_date DATE NOT NULL,

    similar_date DATE NOT NULL,

    similarity_percent NUMERIC(6,2),

    return_1d NUMERIC(10,2),

    return_5d NUMERIC(10,2),

    return_10d NUMERIC(10,2),

    rank_no INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_similarity_date
ON similarity_result(analysis_date);