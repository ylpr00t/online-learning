import Vue from 'vue'
import Router from 'vue-router'
import home from '../components/home.vue'
import myStudy from '../components/myStudy.vue'
import resourceInfo from '../components/resourceInfo.vue'
import resourceShow from '../components/resourceShow.vue'
import myClass from '../components/myClass.vue'
import myClassInfo from '../components/myClassInfo.vue'
import addClass from '../components/addClass.vue'
import myInfo from "../components/myInfo.vue"
import manage from '../components/manage.vue'
import set from '../components/set.vue'
import explain from '../components/explain.vue'

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
          component: manage,
        },
        {
          path: '/manage',
          name: 'manage',
          component: manage
        },
        {
          path: '/myStudy',
          name: 'myStudy',
          component: myStudy
        },
        {
          path: '/resourceInfo',
          name: 'resourceInfo',
          component: resourceInfo
        },
        {
          path: '/resourceShow',
          name: 'resourceShow',
          component: resourceShow
        },
        {
          path: '/myClass',
          name: 'myClass',
          component: myClass
        },
        {
          path: '/myClassInfo',
          name: 'myClassInfo',
          component: myClassInfo
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
          component: set,
        },
        {
          path: '/explain',
          name: 'explain',
          component: explain,
        },
      ]
    },
  ]
})
