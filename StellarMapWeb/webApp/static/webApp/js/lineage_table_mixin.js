const lineage_table_mixin = {
    data() {
      return {
        transProps: {
          // Transition name
          name: 'flip-list',
          account_genealogy_items: {
            type: [Array, Function],
            required: true
          }
        },
        account_genealogy_items: [],
        account_genealogy_fields: [
          { key: 'index', label: 'Index', sortable: true, visible: true },
          { key: 'stellar_creator_account', label: 'Creator Account', sortable: true, visible: false },
          { key: 'stellar_account_created_at', label: 'Account Created At', sortable: true, visible: true },
          { key: 'stellar_account', label: 'Account', sortable: true, visible: true },
          { key: 'network_name', label: 'Network Name', sortable: true, visible: true },
          { key: 'home_domain', label: 'Home Domain', sortable: true, visible: true },
          { key: 'xlm_balance', label: 'XLM Balance', sortable: true, visible: true },
          { key: 'stellar_expert', label: 'Stellar Expert', sortable: true, visible: true },
          { key: 'status', label: 'Status', sortable: true, visible: true }
        ],
        apiStellarExpertTagsResponse: null
      }
    },
    methods: {
      async getAccountGenealogy(stellar_account, network_name) {
          try {
              // Get the CSRF token from the cookie
              const csrf_token = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");

              const headers = {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrf_token
              };
              const genealogy_response = await fetch('/account-genealogy/network/' + network_name + '/stellar_address/' + stellar_account + '/', { method: 'GET', headers });

              if (!genealogy_response.ok) {
                  // Get the error message from the response
                  const error = await genealogy_response.json();
                  throw new Error(error.message);
              }

              // Successful response, do something with the data
              this.account_genealogy_items = JSON.parse(await genealogy_response.json());
              console.log(this.account_genealogy_items);
          } catch (e) {
              // Handle error
              console.error(e);
              alert(e.message);
          }
      },
      truncateStellarAccount(stellar_account) {
        if (stellar_account && stellar_account.length > 17) {
          // return last 6 characters of stellar address
          truncated_string = stellar_account.slice(0, 6) + '...' + stellar_account.slice(-6);
          return truncated_string;
        } else {
          return stellar_account;
        }
      },
      viewExternalLinkStellarExpert(stellar_account, network_name) {
          base_url = "https://stellar.expert/explorer/";
          url_path = base_url.concat(network_name, '/account/', stellar_account);
          return url_path;
      },
      viewTooltipString(string_name) {
        return string_name;
      },
      viewExternalLinkTOML(home_domain) {
        base_url = "https://";
        url_path = base_url.concat(home_domain, '/.well-known/stellar.toml');
        return url_path;
      },
      viewExternalLinkTOMLChecker(home_domain) {
        base_url = "https://stellar.sui.li/";
        url_path = base_url.concat(home_domain);
        return url_path;
      },
      async getStellarExpertTags(stellar_account, network_name) {
        const base_url = "https://api.stellar.expert/explorer/";
        const url_path = base_url.concat(network_name, '/directory/', stellar_account);
        const response = await fetch(url_path);
        const data = await response.json();
        return data;
      }
    },
    computed: {
      visibleGeneologyFields() {
        return this.account_genealogy_fields.filter(field => field.visible)
      },
      apiStellarExpertTagsResponses() {
        // The apiStellarExpertTagsResponses computed property returns an array of promises,
        // one for each row in the table. When each promise resolves, the response data 
        // is stored in the apiStellarExpertTagsResponses array at the same index as the
        // row. In the template, you can access the response data for each row using its index.
        return this.items.map(item => {
          return this.getStellarExpertTags(item.stellar_account, item.network_name);
        });
      }
    }
  }

  