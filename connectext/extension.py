# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Globex Corporation
# All rights reserved.
#
from connect.eaas.extension import (
    Extension,
    ProcessingResponse,
    ValidationResponse,
)

import random
import string


class E2EExtension(Extension):

    def validate_tier_config_setup_request(self, request):
        self.logger.info(f"TCR Validation with id {request['id']}")
        return ValidationResponse.done(request)

    def validate_asset_purchase_request(self, request):
        self.logger.info(f"RTV Validation with if {request['id']}")
        return ValidationResponse.done(request)

    def process_asset_purchase_request(self, request):
        request_id = request['id']
        param_a = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        param_b = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        self.client.requests[request['id']].update(
            {
                "asset": {
                    "params": [
                        {
                            "id": "param_a",
                            "value": param_a
                        },
                        {
                            "id": "param_b",
                            "value": param_b
                        }

                    ]
                }
            }
        )
        self.logger.info("Updating fulfillment parameters as follows:"
                         f"param_a to {param_a} and param_b to {param_b}")
        template_id = self.config['ASSET_REQUEST_APPROVE_TEMPLATE_ID']
        self.logger.info(f'request_id={request_id} - template_id={template_id}')
        self.client.requests[request_id]('approve').post(
            {
                'template_id': template_id,
            }
        )
        return ProcessingResponse.done()

    def process_tier_config_setup_request(self, request):
        self.logger.info(f"Processing request {request['id']}")
        reseller_fulfillment = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        self.client.ns('tier').config_requests[request['id']].update(
            {
                "params": [
                    {
                        "id": "reseller_fulfillment",
                        "value": reseller_fulfillment
                    }
                ]
            }
        )
        self.client.ns('tier').config_requests[request['id']]('approve').post(
            {
                'template': {
                    'id': 'TL-834-966-219'
                }
            }
        )
        return ProcessingResponse.done()
