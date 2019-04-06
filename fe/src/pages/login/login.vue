<template>
  <div id="app">
    <div class="content-box">
      <div class="right-box">
        <div class="login-box">
          <div v-if="flowType === 1">欢迎登录</div>
          <div v-else-if="flowType === 2">立即注册</div>
          <div v-else-if="flowType === 3">重置密码</div>

          <div class="inp-group">
            <label class="label">账户名称</label>
            <input class="inp" placeholder="请输入手机号码" :class="{'focus': focusName}" type="text" v-model="userPhone" @focus="focusName = true" @blur="userPhone === '' ? focusName = false : ''">
          </div>

          <div class="inp-group">
            <label class="label">密码</label>
            <input class="inp" :placeholder="flowType === 3 ? '请输入新密码' : '请输入密码'" :class="{'focus': focusPassword}" type="password" v-model="password" @focus="focusPassword = true" @blur="password === '' ? focusPassword = false : ''">
          </div>

          <div class="inp-group" v-if="flowType === 2 || flowType === 3">
            <label class="label">确认密码</label>
            <input class="inp" :placeholder="flowType === 3 ? '请再次输入新密码' : '请再次输入密码'" :class="{'focus': focusAgainPwd}" type="password" v-model="againPassword" @focus="focusAgainPwd = true" @blur="againPassword === '' ? focusAgainPwd = false : ''">
            <p class="error-tip" v-if="showErrorTip && password !== '' && againPassword !== ''">两次密码输入不一致</p>
          </div>

          <div class="btn-box">
            <label class="label"></label>
            <button class="entry-btn" v-if="flowType === 1" @click="login_func()">登录</button>
            <button class="entry-btn" v-else-if="flowType === 2" @click="red_func()">注册</button>
            <button class="entry-btn" v-else-if="flowType === 3" @click="red_func(2)">修改</button>
            <div class="regFog" v-if="flowType === 1">
              <span class="option mcarloData-btn" @click="flowType = 2;initInp_();">立即注册</span>
              <span class="option mcarloData-btn" @click="flowType = 3;initInp_()">忘记密码</span>
            </div>
            <div class="regFog" v-if="flowType === 2">
              <span class="option mcarloData-btn" @click="flowType = 1;initInp_()">返回登录</span>
              <span class="option mcarloData-btn" @click="flowType = 3;initInp_()">忘记密码</span>
            </div>
            <div class="regFog" v-if="flowType === 3">
              <span class="option mcarloData-btn" @click="flowType = 1;initInp_()">返回登录</span>
              <span class="option mcarloData-btn" @click="flowType = 2;initInp_()">立即注册</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'
  export default {
    name: 'login',
    data () {
      return {
        setInter: null,
        flowType: 1, // 当前流程 1 登录  2 注册  3 修改密码
        userPhone: '', // 用户名
        focusName: false, // 聚焦输入框和输入框有字
        password: '', // 密码
        focusPassword: false,
        againPassword: '', // 再次输入密码
        focusAgainPwd: false,
        focusVer: false,
        // errorTip
        showErrorTip: false, // 两次密码输入不一致
        // regNum: /^\d*$/, // 匹配输入的是否数字
        regPhone: /^[1][3,4,5,6,7,8][0-9]{9}$/, // 验证手机号码格式
        regPassword: /^[0-9a-zA-Z_]{6,12}$/, // 验证密码格式
      }
    },
    beforeCreate() {
      //let token = this.$unit.getCookie('token')
      //if (token) {
      //  this.$unit.jump('manage.html')
      //}
      alert("check token");
    },
    watch: {
      password () {
        if (this.flowType === 2 || this.flowType === 3) {
          if (this.password !== this.againPassword) {
            this.showErrorTip = true
          } else {
            this.showErrorTip = false
          }
        }
      },
      againPassword () {
        if (this.flowType === 2 || this.flowType === 3) {
          if (this.password !== this.againPassword) {
            this.showErrorTip = true
          } else {
            this.showErrorTip = false
          }
        }
      },
    },
    methods: {
      verificationVal_ (type) {
        var message = ''
        if (this.userPhone === '') {
          message = '用户名不能为空'
        }
        if (this.password === '') {
          message = '密码不能为空'
        }
        if (type === 2) { // 验证注册和忘记密码
          if (this.password !== this.againPassword) {
            message = '两次密码输入不一致'
          }
        }
        return message
      },
      initInp_() {
        this.userPhone = ''
        this.password = ''
        this.againPassword = ''
        this.focusName = false
        this.focusPassword = false
        this.focusAgainPwd = false
        this.focusVer = false
        this.showErrorTip = false
      },
      login_func() {
        var message = this.verificationVal_()
        if (message) {
          alert(message)
          return
        }
        this.onClickLogin()
      },
      red_func(type) {
        var message = this.verificationVal_(2)
        if (message) {
          alert(message)
          return
        }
        if (type === 2) { // 修改
          this.onClickEditPwd_()
        }
        this.onClickRegister_()
      },
      onClickLogin () {
        var request = {
          'username': this.userPhone,
          'password': this.password,
        }
        $.ajax({
          type:"POST",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(request),
          dataType: "json",
          url:"http://localhost:8081/api/login",
          /*
          beforeSend: function(request) {
            request.setRequestHeader("Authorization", "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwibmJmIjoxNTUyNzQ3Nzg3LCJleHAiOjE1NTI3NzY1ODcsImlhdCI6MTU1Mjc0Nzc4N30.0sJbtLQIzRWtB0Wm4ZPQSIooGyWSFE_JrxsbR9p2UUw");
          },
          */
          success:function (data) {
            if (data['code'] == -400)
              alert(data['message'])
            else if (data['code'] == 0){
              alert(data['message'])
              //存储token，跳转到manage.html
              //this.storageCookie_func(request.username, request.password, data['data']['access_token'])
              var exdate = new Date()
              exdate.setDate(exdate.getDate() + (99) || 0)
              document.cookie = 'username' + '=' + escape(request.username) + ';expires=' + exdate.toGMTString()
              document.cookie = 'password' + '=' + escape(request.password) + ';expires=' + exdate.toGMTString()
              document.cookie = 'token' + '=' + escape(data['data']['access_token']) + ';expires=' + exdate.toGMTString()
              window.location.href = "manage.html"
            }
          },
          error:function (e) {
            alert("500");
          }
        });
      },

      onClickRegister_ () {
        alert("register")
        /*
        var request = {
          'username': this.userPhone,
          'password': this.password,
        }
        this.$http({
          url: registerUrl,
          method: 'post',
          data: request,
          that: this
        }).then((response) => {
          this.scStatis_(request.username, 'register')
          this.$root.$refs.tip.show_('注册成功')
          this.flowType = 1
          this.initInp_()
          return Promise.resolve()
        })
        */
      },
      onClickEditPwd_ () {
        alert("change pass")
        /*
        var request = {
          'username': this.userPhone,
          'password': this.password,
        }
        this.$http({
          url: resetPwdUrl,
          method: 'post',
          data: request,
          that: this
        }).then((response) => {
          this.$root.$refs.tip.show_('修改密码成功')
          this.initInp_()
          this.flowType = 1
          return Promise.resolve()
        })
        */
      },
    },
  }
</script>


<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>
