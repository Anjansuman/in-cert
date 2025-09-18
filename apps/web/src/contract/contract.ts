/**
 * Program IDL in camelCase format in order to be used in JS/TS.
 *
 * Note that this is only a type helper and is not the actual IDL. The original
 * IDL can be found at `target/idl/contract.json`.
 */
export type Contract = {
  "address": "9nF17epkj1esEvgx4JpkviUfn2XbEheBDUsiuqAt6ogc",
  "metadata": {
    "name": "contract",
    "version": "0.1.0",
    "spec": "0.1.0",
    "description": "Created with Anchor"
  },
  "instructions": [
    {
      "name": "createCertificate",
      "discriminator": [
        238,
        189,
        143,
        29,
        100,
        80,
        70,
        10
      ],
      "accounts": [
        {
          "name": "certificate",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  99,
                  101,
                  114,
                  116,
                  105,
                  102,
                  105,
                  99,
                  97,
                  116,
                  101
                ]
              },
              {
                "kind": "arg",
                "path": "institutionId"
              },
              {
                "kind": "arg",
                "path": "candidateId"
              },
              {
                "kind": "arg",
                "path": "issuedAt"
              }
            ]
          }
        },
        {
          "name": "authority",
          "writable": true,
          "signer": true
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": [
        {
          "name": "institutionId",
          "type": "string"
        },
        {
          "name": "institutionName",
          "type": "string"
        },
        {
          "name": "candidateId",
          "type": "string"
        },
        {
          "name": "candidateName",
          "type": "string"
        },
        {
          "name": "issuedAt",
          "type": "i64"
        },
        {
          "name": "description",
          "type": "string"
        },
        {
          "name": "uri",
          "type": {
            "option": "string"
          }
        }
      ]
    }
  ],
  "accounts": [
    {
      "name": "certificate",
      "discriminator": [
        202,
        229,
        222,
        220,
        116,
        20,
        74,
        67
      ]
    }
  ],
  "types": [
    {
      "name": "certificate",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "institution",
            "type": "pubkey"
          },
          {
            "name": "institutionId",
            "type": "string"
          },
          {
            "name": "institutionName",
            "type": "string"
          },
          {
            "name": "candidateId",
            "type": "string"
          },
          {
            "name": "candidateName",
            "type": "string"
          },
          {
            "name": "issuedAt",
            "type": "i64"
          },
          {
            "name": "description",
            "type": "string"
          },
          {
            "name": "uri",
            "type": {
              "option": "string"
            }
          }
        ]
      }
    }
  ]
};
