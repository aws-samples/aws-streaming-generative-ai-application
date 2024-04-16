package com.amazonaws.flink.async.bedrock.operators;

import org.apache.flink.connector.opensearch.sink.OpensearchSink;
import org.apache.flink.connector.opensearch.sink.OpensearchSinkBuilder;
import org.apache.http.HttpHost;
import org.opensearch.action.index.IndexRequest;
import org.opensearch.client.Requests;
import org.opensearch.common.xcontent.XContentType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Sink to write data to Amazon OpenSearch Service.
 */
public class AmazonOpenSearchSink {

    private static final Logger LOG = LoggerFactory.getLogger(AmazonOpenSearchSink.class);


    /**
     * Creates an IndexRequest for the given element to index.
     * 
     * @param element the element to index
     * @param index the target index name
     * @param <T> the type of element
     * @return the IndexRequest
     */
    private static <T> IndexRequest createIndexRequest(T element, String index) {
        LOG.info("Element: " + element.toString());
        return Requests.indexRequest()
                .index(index)
                .source(element.toString(), XContentType.JSON);
    }

    /**
     * Builds an OpenSearch sink to the given endpoint and index.
     *
     * @param openSearchEndpoint the OpenSearch endpoint URL
     * @param indexName the target index name
     * @param <T> the type of elements
     * @return the OpenSearch sink
     */
    public static <T> OpensearchSink<T> buildOpenSearchSink(String openSearchEndpoint, String indexName) {
        final HttpHost host = HttpHost.create(openSearchEndpoint);
        return new OpensearchSinkBuilder<T>()
                .setHosts(host)
                .setEmitter(
                        (element, context, indexer) ->
                                indexer.add(createIndexRequest(element, indexName)))
                .build();
    }
}
