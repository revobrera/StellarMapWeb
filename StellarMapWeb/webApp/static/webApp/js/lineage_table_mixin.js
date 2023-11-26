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
          { key: 'status', label: 'Status', sortable: true, visible: true },
          { key: 'updated_at', label: 'Updated At', sortable: true, visible: true }
        ],
        apiStellarExpertTagsResponses: [],
        tree_genealogy_items: null
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
              const response = await genealogy_response.json();

              console.log(response);

              if ('account_genealogy_items_json' in response) {
                this.account_genealogy_items = response['account_genealogy_items_json'];
                console.log(this.account_genealogy_items);
              } else {
                console.log('account_genealogy_items_json not found in response');
              }

              if ('tree_genealogy_items_json' in response) {
                this.tree_genealogy_items = response['tree_genealogy_items_json'];
                console.log(this.tree_genealogy_items);
              } else {
                console.log('tree_genealogy_items_json not found in response');
              }

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
      async getApiStellarExpertTags(row_index, stellar_account, network_name) {
        const base_url = "https://api.stellar.expert/explorer/";
        const url_path = base_url.concat(network_name, '/directory/', stellar_account);
        const response = await fetch(url_path);
        this.apiStellarExpertTagsResponses[row_index] = await response.json();
        return this.apiStellarExpertTagsResponses[row_index];
      },
      formatHashtag(tag) {
        hashtag = '#';
        return hashtag.concat(tag);
      }
    },
    computed: {
      visibleGeneologyFields() {
        return this.account_genealogy_fields.filter(field => field.visible)
      }
    },
    watch: {
      account_genealogy_items: {
        deep: true,
        handler(newVal, oldVal) {
          if (newVal !== oldVal) {
            newVal.forEach((item) => {
              this.getApiStellarExpertTags(item.index, item.stellar_account, item.network_name);
            });
          }
        },
      },
    }
  }

  