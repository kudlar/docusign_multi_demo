#!/usr/bin/python
# -*- coding: utf-8 -*-
# DocuSign API Multiple Documents Recipe 012 (PYTHON)

# Set encoding to utf8. See http://stackoverflow.com/a/21190382/64904

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
import socket
import certifi
import requests
import os
import base64
import re
import urllib
import shutil

# See http://requests.readthedocs.org/ for information on the requests library
# See https://urllib3.readthedocs.org/en/latest/security.html for info on making secure https calls
# in particular, run pip install certifi periodically to pull in the latest cert bundle

from lib_master_python import ds_recipe_lib
from flask import request

# Enter your info here
# Or set environment variables DS_USER_EMAIL, DS_USER_PW, and DS_INTEGRATION_ID
# Globals:

ds_user_email = '***'
ds_user_pw = '***'
ds_integration_id = '***'
ds_account_id = False
doc_document_path = 'app/static/sample_documents_master/NDA.pdf'
doc_document_name = 'NDA.pdf'
doc2_document_path = 'app/static/sample_documents_master/House.pdf'
doc2_document_name = 'House.pdf'
doc3_document_path = \
    'app/static/sample_documents_master/contractor_agreement.docx'
doc3_document_name = 'contractor_agreement.docx'
webhook_path = '/webhook'
ds_signer1_email = '***'
ds_signer1_name = '***'
ds_cc1_email = '***'
ds_cc1_name = '***'
xml_file_dir = 'app/files/'
readme = 'ReadMe.txt'


def send():
    global ds_account_id, ds_signer1_email, ds_signer1_name, \
        ds_cc1_email, ds_cc1_name
    msg = ds_recipe_lib.init(ds_user_email, ds_user_pw,
                             ds_integration_id, ds_account_id)
    if msg != None:
        return {'ok': False, 'msg': msg}

    # Ready...
    # Possibly create some fake people
    # ds_signer1_email = ds_recipe_lib.get_signer_email(ds_signer1_email)
    # ds_signer1_name = ds_recipe_lib.get_signer_name(ds_signer1_name)
    # ds_cc1_email = ds_recipe_lib.get_signer_email(ds_cc1_email)
    # ds_cc1_name = ds_recipe_lib.get_signer_name(ds_cc1_name)

    ds_signer1_email = 'rastok@gmail.com'
    ds_signer1_name = 'Signer 1'
    ds_signer2_email = 'rasto@grownapps.io'
    ds_signer2_name = 'Signer 2'
    ds_cc1_email = 'rasto@grownapps.io'
    ds_cc1_name = 'Carbon Copy'

    # STEP 1 - Login

    r = ds_recipe_lib.login()
    if not r['ok']:
        return r
    ds_account_id = ds_recipe_lib.ds_account_id

    #
    # STEP 2 - Create and send envelope
    #

    # construct the body of the request

    file_contents = open(doc_document_path, 'rb').read()
    file2_contents = open(doc2_document_path, 'rb').read()
    file3_contents = open(doc3_document_path, 'rb').read()

    # Please use the most accurate and relevant subject line.

    subject = 'Please sign the house documentation package'

    # File contents are provided here
    # The documents array can include multiple documents, of differing types.
    # All documents are converted to pdf prior to signing.
    # The fileExtension field defaults to "pdf".

    documents1 = [{
        'documentId': '1',
        'name': doc_document_name,
        'fileExtension': (os.path.splitext(doc_document_path)[1])[1:],
        'documentBase64': base64.b64encode(file_contents),
        }, {
        'documentId': '2',
        'name': doc2_document_name,
        'fileExtension': (os.path.splitext(doc2_document_path)[1])[1:],
        'documentBase64': base64.b64encode(file2_contents),
        }]

    documents2 = [{
        'documentId': '1',
        'name': doc_document_name,
        'fileExtension': (os.path.splitext(doc_document_path)[1])[1:],
        'documentBase64': base64.b64encode(file_contents),
        }, {
        'documentId': '3',
        'name': doc3_document_name,
        'fileExtension': (os.path.splitext(doc3_document_path)[1])[1:],
        'documentBase64': base64.b64encode(file3_contents),
        }]

    # The signing fields
    #
    # Invisible (white) Anchor field names for the NDA.pdf document:
    #   * signer1sig
    #   * signer1name
    #   * signer1company
    #   * signer1date
    #
    # Explicitly placed fields are used in the contractor_agreement
    # and on the house diagram
    #
    # Some anchor fields for document 3, the contractor_agreement.docx, use existing 
    # content from the document:
    #   * "Client Signature"
    #   * "Client Name"
    # 
    # NOTE: Anchor fields search ALL the documents in the envelope for
    # matches to the field's anchor text
    fields1 = {
    "signHereTabs": [{
        "anchorString": "signer1sig", # Anchored for doc 1
        "anchorXOffset": "0",
         "anchorYOffset": "0",
        "anchorUnits": "mms",
        "recipientId": "1",
        "name": "Please sign here",
        "optional": "false",
        "scaleValue": 1,
        "tabLabel": "signer1sig"},
        {
        "documentId": "2", # Explicit position for doc 2
        "pageNumber": "1",
        "recipientId": "2",
        "xPosition": "89",
        "yPosition": "40",
        "name": "Please sign here",
        "optional": "false",
        "scaleValue": 1,
        "tabLabel": "signer1_doc2"}],
    "fullNameTabs": [{
        "anchorString": "signer1name", # Anchored for doc 1
         "anchorYOffset": "-6",
        "fontSize": "Size12",
        "recipientId": "1",
        "tabLabel": "Full Name",
        "name": "Full Name"}],
    "textTabs": [{                 
        "anchorString": "signer1company", # Anchored for doc 1
         "anchorYOffset": "-8",
        "fontSize": "Size12",
        "recipientId": "1",      # Because the same tab label is 
        "tabLabel": "Company",   # used, these fields will have duplicate data
        "name": "Company",       # Note that the account's "Data Population Scope"
        "required": "true"},     # must be set to "Envelope" to enable this feature.
        ],
    "dateSignedTabs": [{
        "anchorString": "signer1date", # Anchored for doc 1
        "anchorYOffset": "-6",
        "fontSize": "Size12",
        "recipientId": "1",
        "name": "Date Signed",
        "tabLabel": "date_signed"},
        {
        "documentId": "2", # Explicit position for doc 2
        "pageNumber": "1",
        "recipientId": "1",
        "xPosition": "89",
        "yPosition": "100",
        "fontSize": "Size12",
        "recipientId": "1",
        "name": "Date Signed",
        "tabLabel": "doc3_date_signed"}]
    }
	
	fields2 = {
    "signHereTabs": [{
        "anchorString": "signer1sig", # Anchored for doc 1
        "anchorXOffset": "0",
         "anchorYOffset": "0",
        "anchorUnits": "mms",
        "recipientId": "1",
        "name": "Please sign here",
        "optional": "false",
        "scaleValue": 1,
        "tabLabel": "signer1sig"},
        {
        "anchorString": "Client Signature", # Anchored for doc 3
        "anchorXOffset": "0",
         "anchorYOffset": "-4",
        "anchorUnits": "mms",
        "recipientId": "1",
        "name": "Please sign here",
        "optional": "false",
        "scaleValue": 1,
        "tabLabel": "doc3_client_sig"}],
    "fullNameTabs": [{
        "anchorString": "signer1name", # Anchored for doc 1
         "anchorYOffset": "-6",
        "fontSize": "Size12",
        "recipientId": "1",
        "tabLabel": "Full Name",
        "name": "Full Name"}],
    "textTabs": [{                 
        "anchorString": "signer1company", # Anchored for doc 1
         "anchorYOffset": "-8",
        "fontSize": "Size12",
        "recipientId": "1",      # Because the same tab label is 
        "tabLabel": "Company",   # used, these fields will have duplicate data
        "name": "Company",       # Note that the account's "Data Population Scope"
        "required": "true"},     # must be set to "Envelope" to enable this feature.
        {
        "anchorString": "Client Name", # Anchored for doc 3
        "anchorYOffset": "-38",
        "fontSize": "Size12",
        "recipientId": "1",
        "tabLabel": "Company",  
        "name": "Company",      
        "required": "true"},    
        {
        "documentId": "3", # Explicit position for doc 3
        "pageNumber": "1",
        "recipientId": "1",
        "xPosition": "145",
        "yPosition": "195",
        "fontSize": "Size10",
        "required": "true",
        "tabLabel": "Company",
        "name": "Company"}],
    "dateSignedTabs": [{
        "anchorString": "signer1date", # Anchored for doc 1
        "anchorYOffset": "-6",
        "fontSize": "Size12",
        "recipientId": "1",
        "name": "Date Signed",
        "tabLabel": "date_signed"}
        ]
    }

    signers1 = [{
        'email': ds_signer1_email,
        'name': ds_signer1_name,
        'recipientId': '1',
        'routingOrder': '1',
        'tabs': fields1,
        }]

    signers2 = [{
        'email': ds_signer2_email,
        'name': ds_signer2_name,
        'recipientId': '2',
        'routingOrder': '2',
        'tabs': fields2,
        }]

    ccs = [{
        'email': ds_cc1_email,
        'name': ds_cc1_name,
        'recipientId': '3',
        'routingOrder': '3',
        }]

    data1 = {
        'emailSubject': subject,
        'documents': documents1,
        'recipients': {'signers': signers1, 'carbonCopies': ccs},
        'status': 'sent',
        }

    data2 = {
        'emailSubject': subject,
        'documents': documents2,
        'recipients': {'signers': signers2, 'carbonCopies': ccs},
        'status': 'sent',
        }

    # append "/envelopes" to the baseUrl and use in the request

    url = ds_recipe_lib.ds_base_url + '/envelopes'
    try:
        r = requests.post(url, headers=ds_recipe_lib.ds_headers,
                           json=data1)
    except requests.exceptions.RequestException, e:
        return {'ok': False, 'msg': 'Error calling Envelopes:create: ' \
                + str(e)}

    try:
        r2 = requests.post(url, headers=ds_recipe_lib.ds_headers,
                           json=data2)
    except requests.exceptions.RequestException, e:
        return {'ok': False, 'msg': 'Error calling Envelopes:create: ' \
                + str(e)}

    # ####################################################################

    status = r.status_code
    if status != 201:
        return {'ok': False,
                'html': '<h3>Error calling DocuSign Envelopes:create</h3><p>Status is: ' \
                + str(status) + '. Response: </p><pre><code>' + r.text \
                + '</code></pre>'}

    data = r.json()
    envelope_id = data['envelopeId']

    # Instructions for reading the email

    html = '<h2>Signature request sent!</h2>' + '<p>Envelope ID: ' \
        + envelope_id + '</p>' + '<p>Signer: ' + ds_signer1_name \
        + '</p>' + '<p>CC: ' + ds_cc1_name + '</p>' \
        + '<h2>Next step:</h2>' \
        + '<h3>Respond to the Signature Request</h3>'

    ds_signer1_email_access = \
        ds_recipe_lib.get_temp_email_access(ds_signer1_email)
    if ds_signer1_email_access:

        # A temp account was used for the email

        html += \
            '<p>Respond to the request via your mobile phone by using the QR code: </p>' \
            + '<p>' \
            + ds_recipe_lib.get_temp_email_access_qrcode(ds_signer1_email_access) \
            + '</p>' + "<p> or via <a target='_blank' href='" \
            + ds_signer1_email_access + "'>your web browser.</a></p>"
    else:

        # A regular email account was used

        html += \
            '<p>Respond to the request via your mobile phone or other mail tool.</p>' \
            + '<p>The email was sent to ' + ds_signer1_name + ' <' \
            + ds_signer1_email + '></p>'

    return {
        'ok': True,
        'envelope_id': envelope_id,
        'ds_signer1_email': ds_signer1_email,
        'ds_signer1_name': ds_signer1_name,
        'ds_signer1_access': ds_signer1_email_access,
        'ds_signer1_qr': ds_signer1_email,
        'ds_cc1_email': ds_cc1_email,
        'ds_cc1_name': ds_cc1_name,
        'html': html,
        }


########################################################################
########################################################################

# FIN


			