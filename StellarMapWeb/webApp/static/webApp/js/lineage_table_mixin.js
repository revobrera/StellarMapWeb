const lineage_table_mixin = {
    data() {
      return {
        transProps: {
          // Transition name
          name: 'flip-list'
        },
        items: [
          { Active: 'Account (active)', Created: '05/06/2021', Account: 'YUIB' },
          { Active: 'Account (active)', Created: '06/03/2021', Account: 'UIBC' },
          { Active: 'Account (active)', Created: '06/17/2021', Account: 'OPIU' },
          { Active: 'Account (disabled)', Created: '07/17/2021', Account: 'MNUB' }
        ],
        fields: [
          { key: 'Active', sortable: true },
          { key: 'Created', sortable: true },
          { key: 'Account', sortable: true },
          { key: 'Home Domain', sortable: true },
          { key: 'XLM Balance', sortable: true },
          { key: 'Stellar.Expert', sortable: true }
        ],
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
      async testMethod() {
        // Do something here
        await someAsyncFunction();
        console.log("This is a test method");
      }
    }
  }

  