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
          { key: 'index', label: 'Index', sortable: true },
          { key: 'stellar_creator_account', label: 'Creator Account', sortable: true },
          { key: 'stellar_account_created_at', label: 'Account Created At', sortable: true },
          { key: 'stellar_account', label: 'Account', sortable: true },
          { key: 'network_name', label: 'Network Name', sortable: true },
          { key: 'home_domain', label: 'Home Domain', sortable: true },
          { key: 'xlm_balance', label: 'XLM Balance', sortable: true },
          { key: 'stellar_expert', label: 'Stellar Expert', sortable: true },
          { key: 'status', label: 'Status', sortable: true }
        ]
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
      }
    }
  }

  