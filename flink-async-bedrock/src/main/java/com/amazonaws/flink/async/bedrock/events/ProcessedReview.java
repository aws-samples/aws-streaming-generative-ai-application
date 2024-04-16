package com.amazonaws.flink.async.bedrock.events;

public class ProcessedReview {

    private int reviewId;
    private String userId;
    private String summary;
    private long dateTime;
    private String sentiment;

    public ProcessedReview() {
    }

    public ProcessedReview(int reviewId, String userId, String summary, long dateTime, String sentiment) {
        this.reviewId = reviewId;
        this.userId = userId;
        this.summary = summary;
        this.dateTime = dateTime;
        this.sentiment = sentiment;
    }

    public int getReviewId() {
        return reviewId;
    }

    public void setReviewId(int reviewId) {
        this.reviewId = reviewId;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String productId) {
        this.summary = summary;
    }

    public long getDateTime() {
        return dateTime;
    }
    public void setDateTime(long dateTime) {
        this.dateTime = dateTime;
    }

    public String getSentiment() { return  sentiment; }

    public void setSentiment(String sentiment) { this.sentiment = sentiment; }

    @Override
    public String toString() {
        return "ProcessedReview{" +
                "reviewId=" + reviewId +
                ", userId='" + userId + '\'' +
                ", summary='" + summary + '\'' +
                ", dateTime=" + dateTime + '\'' +
                ", sentiment=" + sentiment +
                '}';
    }
}
