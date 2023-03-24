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
      testMethod() {
        // Do something here
        // await someAsyncFunction();
        console.log("This is a test method");
      }
    }
  }

  