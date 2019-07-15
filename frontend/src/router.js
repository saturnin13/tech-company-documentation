import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Markdown from './views/Markdown.vue'
import BrowserView from './views/BrowserView.vue'
import Documents from './views/Documents.vue'
import Login from './views/Login.vue'
import AuthGithubCallback from "./views/AuthGithubCallback";
import Installs from "./views/Installs";
import AppInstallationCallbackGithub from "./views/AppInstallationCallbackGithub";
import AuthGithub from "./views/AuthGithub";

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/:account_id/markdown',
      name: 'markdown',
      component: Markdown
    },
    {
      path: '/:account_id/browser',
      name: 'browser',
      component: BrowserView
    },
    {
      path: '/:account_id/docs',
      name: 'docs',
      component: Documents
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/auth/github',
      name: 'auth_github',
      component: AuthGithub
    },
    {
      path: '/auth/github/callback',
      name: 'auth_github_callback',
      component: AuthGithubCallback
    },
    {
      path: '/installs',
      name: 'installs',
      component: Installs
    },
    {
      path: '/auth/github/app_installation_callback',
      name: 'auth_github_app_installation_callback',
      component: AppInstallationCallbackGithub
    }
  ]
})
