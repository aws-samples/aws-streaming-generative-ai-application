#!/usr/bin/env node

/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

import { App }from 'aws-cdk-lib';
import { MainStack } from '../lib/main';

const app = new App();

const stack = new MainStack(app, 'StreamingGenerativeAIStack', {
    kinesisStreamName: 'generative-ai-stream',
    flinkAppName: 'generative-ai-flink-application',
    openSearchDomainName: 'generative-ai-opensearch'
});





