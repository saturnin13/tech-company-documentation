// initial state
const state = {
  names: []
};

// getters
const getters = {};

// actions
const actions = {};

// mutations
const mutations = {
  setInstallations (state, installations) {
    state.names = installations;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
