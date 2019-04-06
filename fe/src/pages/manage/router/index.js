import Vue from 'vue'
import Router from 'vue-router'
import home from '../components/home.vue'
import myStudy from '../components/myStudy.vue'
import addStudy from '../components/addStudy.vue'
import myClass from '../components/myClass.vue'
import addClass from '../components/addClass.vue'
import myInfo from "../components/myInfo";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home,
      children: [
        {
          path: '/',
          name: 'home',
          component: home,
        },
        {
          path: '/myStudy',
          name: 'myStudy',
          component: myStudy
        },
        {
          path: '/addStudy',
          name: 'addStudy',
          component: addStudy
        },
        {
          path: '/myClass',
          name: 'myClass',
          component: myClass
        },
        {
          path: '/addClass',
          name: 'addClass',
          component: addClass
        },
        {
          path: '/myInfo',
          name: 'myInfo',
          component: myInfo
        },
        {
          path: '/set',
          name: 'set',
          component: home,
        },
        {
          path: '/explain',
          name: 'explain',
          component: home,
        }
      ]
    },
  ]
})
