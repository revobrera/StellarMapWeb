// https://json-generator.com/
{
    name: '{{lorem(1, "words").toUpperCase()}}',
    node_type: 'ISSUER',
    issuer_id: '{{objectId().toUpperCase()}}',
    description: '{{lorem(3, "words")}}',
    url: '{{random("google.co", "yahoo.com", "qwant.com")}}',
    created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
    deleted: '{{random(false, false, false, false, false, false, false, false, true)}}',
    children: [
            '{{repeat(3, 9)}}',
            {
            name: '{{lorem(1, "words").toUpperCase()}}',
            node_type: 'ISSUER',
            issuer_id: '{{objectId().toUpperCase()}}',
            description: '{{lorem(6, "words")}}',
            url: '{{random("google.co", "yahoo.com", "qwant.com")}}',
            created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
            deleted: '{{random(false, false, false, false, false, false, false, false, true)}}',
            children: [
                '{{repeat(9, 17)}}',
                {
                name: '{{lorem(1, "words").toUpperCase()}}',
                node_type: 'ISSUER',
                issuer_id: '{{objectId().toUpperCase()}}',
                description: '{{lorem(3, "words")}}',
                url: '{{random("google.co", "yahoo.com", "qwant.com")}}',
                created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
                deleted: '{{random(false, false, false, false, false, false, false, false, true)}}',
                children: [
                    '{{repeat(0, 3)}}',
                    {
                    name: '{{lorem(1, "words").toUpperCase()}}',
                    node_type: 'ISSUER',
                    issuer_id: '{{objectId().toUpperCase()}}',
                    description: '{{lorem(17, "words")}}',
                    url: '{{random("google.co", "yahoo.com", "qwant.com")}}',
                    created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
                    deleted: '{{random(false, false, false, false, false, false, false, false, true)}}'
                    }
                ]
                }
            ]
            }	
        ]
    }
    
    
    
    

// asset_records
    [
        '{{repeat(1, 96)}}',
        {
          _links: {
            toml: {
              href: 'https://www.domain-name.com/.well-known/s.toml'
            }
          },
          issuer_id: '{{objectId().toUpperCase()}}',
          name: '{{random("ABC", "DEF", "GHI", "JKL", "MNO", "PQR", "STU", "VWX", "YZ0")}}',
          node_type: 'ASSET',
          asset_type: '{{random("credit_alphanum4", "native", "native")}}',
          asset_code: '{{random("ABC", "DEF", "GHI", "JKL", "MNO", "PQR", "STU", "VWX", "YZ0")}}',
          num_accounts: '{{integer(0, 963369)}}',
          num_claimable_balances: '{{integer(3, 96)}}',
          num_liquidity_pools: '{{integer(0, 369)}}',
          amount: '{{floating(0.000001, 369369369.003)}}',
          flags: {
            auth_required: '{{random(false, false, false, false, false, false, false, false, true)}}',
            auth_revocable: '{{random(false, false, false, false, false, false, false, false, true)}}',
            auth_immutable: '{{random(false, false, false, false, false, false, false, false, true)}}',
            auth_clawback_enabled: '{{random(false, false, false, false, false, false, false, false, true)}}'
          }
        }
    ]
