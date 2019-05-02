<template>
  <div id="app">
    <div class="content-box">
      <div class="right-box">
        <div class="login-box">
          <div v-if="flowType === 1" class="login-title">欢迎登录</div>
          <div v-else-if="flowType === 2" class="login-title">立即注册</div>
          <div v-else-if="flowType === 3" class="login-title">重置密码</div>

          <div class="inp-group">
            <label class="label">账户名称</label>
            <input class="inp" placeholder="请输入手机号码" :class="{'focus': focusName}" type="text" v-model="userPhone" @focus="focusName = true" @blur="userPhone === '' ? focusName = false : ''">
          </div>

          <div class="inp-group">
            <label class="label">账户密码</label>
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
        showErrorTip: false, // 两次密码输入不一致
        regPhone: /^[1][3,4,5,6,7,8][0-9]{9}$/, // 验证手机号码格式
        regPassword: /^[0-9a-zA-Z_]{6,12}$/, // 验证密码格式
      }
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
          alert('当前版本不开放次功能，请联系管理员吧')
          return
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
          success:function (data) {
            if (data['code'] == -400)
              alert(data['message'])
            else if (data['code'] == 0){
              alert(data['message'])
              var exdate = new Date()
              exdate.setDate(exdate.getDate() + (99) || 0)
              document.cookie = 'username' + '=' + escape(request.username) + ';expires=' + exdate.toGMTString()
              document.cookie = 'password' + '=' + escape(request.password) + ';expires=' + exdate.toGMTString()
              document.cookie = 'token' + '=' + escape(data['data']['access_token']) + ';expires=' + exdate.toGMTString()
              window.location.href = "manage.html"
            }
          },
          error:function (e) {
            alert("服务器内部出错了，请稍等!!!");
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
    },
  }
</script>


<style lang="stylus" scoped>
  body{text-align:center}
  #app
    width 100%
    height 100%
    overflow hidden
    .content-box
      width 100%
      height 100%
      overflow auto
      align-items center
      .right-box
        margin 0 auto
        flex 0 0 45%
        height 100%
        width 50%
        min-width 600px
        min-height 650px
        background #f0f0f0
        position relative
        .login-box
          width 100%
          position absolute
          top 50%
          left 50%
          transform translate3d(-50%, -50%, 0)
          padding 0 15%
          box-sizing border-box
          .login-title
            text-align center
            margin-bottom 15%
            margin-left 15%
            font-size 30px
            color #000000
          .inp-group
            width 100%
            margin-bottom 30px
            display flex
            align-items center
            justify-content space-between
            position relative
            .label
              flex 0.2
              text-align right
              margin-right 15px
              color #000000
              font-size 16px
            .inp
              flex 1
              padding 10px 0
              text-indent 10px
              background #ffffff
              opacity 0.5
              border-radius 2px
              &.focus
                opacity 1
            .inp.verifcation-inp
              border-radius 2px 0 0 2px
            .inp-box
              flex 1
              overflow hidden
              display flex
              .btn
                padding 0 10px
                color #343434
                background #ffffff
                outline none
                cursor pointer
            .inp-box.protocol
              display flex
              align-items center
              .radio
                width 15px
                height 15px
                cursor pointer
                margin-right 10px
                background #ffffff
                img
                  width 100%
                  height 100%
                  margin 50% 0 0 50%
                  transform translate3d(-50%, -50%, 0)
              .protocol-text
                cursor pointer
                font-size 12px
                color #ffffff
                font-weight 200
                text-decoration underline
              .radio.slct
                background #ff5f3d
            .error-tip
              font-size 12px
              color #ff2020
              position absolute
              top 50%
              right 20px
              transform translateY(-50%)
          .btn-box
            width 100%
            display flex
            text-align center
            margin-top 30px
            position relative
            .label
              flex 0.2
              margin-right 15px
            .entry-btn
              flex 1
              height 38px
              line-height 38px
              cursor pointer
              outline none
              border-radius 2px
              background #ff5f3d
              text-align center
              color #ffffff
              font-size 18px
              &:hover
                box-shadow 0 5px 8px 0 rgba(255,95,61,0.50)
              &:active
                background #EB4B29
            .regFog
              width 80%
              position absolute
              top 150%
              left 20%
              display flex
              justify-content space-around
              .option
                font-size 14px
                text-decoration underline
                font-weight 200
                color #000000
                cursor pointer
                opacity 0.7
                &:hover
                  color #ff5f3d
          .acconut-box, .password-box, .code-box
            display flex
            margin-bottom 24px
            padding-bottom 14px
            padding-left 28px
            border-bottom 1px solid #8E9191
            position relative
            .acconut, .password, .code
              margin-left 44px
              height 30px
              font-size 20px
              color #8E9191
              -webkit-appearance none
              -moz-appearance textfield
            .acconut::-webkit-outer-spin-button,
            .acconut::-webkit-inner-spin-button
              -webkit-appearance none
            .acconut, .password
              width 422px
            .code
              width 322px
            .code-btn
              width 100px
              color #FFB822
              background-color #fff
              cursor pointer
            .passwordTip
              position absolute
              right 0
              width 200px
              height 40px
              top 0
              background-size 100% 100%
              padding 12px 0
              padding-left 30px
              box-sizing border-box
              color red
          .password-box, .code-box
            img
              padding 1px 0
          .acconut-box.
            img
              padding 3px 0
          .active-box
            border-bottom 1px solid #FFB822
          .login-btn
            margin 100px auto 24px
            width 250px
            padding 12px 0
            border-radius 6px
            box-shadow 1px 3px 4px 2px rgba(255,184,34,.4)
            font-size 16px
            text-align center
            color #ffffff
            background-color #FFB822
            cursor pointer
            &.is-danger
              background-color #eaeaea
              box-shadow none
              cursor not-allowed
          .tip
            padding-bottom 4px
            font-size 14px
            width 50%
            margin auto
            color #ffffff
            cursor pointer
            display flex
            justify-content space-around
            & span
              border-bottom 1px solid #ffffff
            & span:hover
              color #FFB822
              border-bottom 1px solid #FFB822
        .register-box
          padding-left 28px
          padding-bottom 14px
          border-bottom 1px solid #8e9191
          display flex
        .register-box input
          height 30px
          font-size 20px
          color #8e9191
          margin-left 44px
        .register-box span
          cursor pointer
          line-height 30px
          text-align center
          min-width 80px
        .scan-code
          display flex
          position absolute
          bottom 60px
          left 50%
          transform translateX(-50%)
          justify-content space-between
          width 40%
          text-align center
          font-size 14px
          color #828282
        .help-book
          position absolute
          right 100px
          top 20px
          cursor pointer
          &:hover
            color #FFB822
</style>
<style lang="stylus">
  .nc_scale
    height 38px !important
    background #E8E8E8 !important
    div.nc_bg
      background #FFB822 !important
    .scale_text
      font-size 15px !important
    .scale_text2
      color #FFF !important
    span.btn_slide
      border 1px solid #FFF !important
  .errloading
    border #FAF1D5 1px solid !important
    color #EF9F06 !important
  .nc-container
    border 0
    border-radius 2px
    overflow hidden
    width 100% !important
    #nc_2_wrapper, #nc_2_wrapper
      width 100% !important
    .imgCaptcha, .clickCaptcha
      width 100% !important
  .nc-container .nc_scale span
    height 36px
    line-height 36px
</style>
