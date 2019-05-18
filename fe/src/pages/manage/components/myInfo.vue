<template>
    <div>
      <i class="el-icon-goods">用户信息</i>
      <hr/>
      <div id="main-contain">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="用户名">
            <label>{{username}}</label>
          </el-form-item>
          <el-form-item label="ECOIN">
            <label>{{e_coin}}</label>
          </el-form-item>
          <el-form-item label="真实姓名">
            <label>{{realname}}</label>
          </el-form-item>
          <el-form-item label="电子邮箱">
            <label>{{useremail}}</label>
          </el-form-item>
          <el-form-item label="详细地址">
            <label>{{useraddress}}</label>
          </el-form-item>
          <!--
          <el-form-item label="在学课程">
            <label>{{classes_sum}}</label>
          </el-form-item>
          <el-form-item label="涉及领域">
            <label>{{category}}</label>
          </el-form-item>
          -->
        </el-form>
      </div>
    </div>
</template>

<script>
    import $ from 'jquery'
    export default {
      name: "myInfo",
      data() {
        return {
          username: '',
          realname: '',
          useremail: '',
          useraddress: '',
          e_coin: 0,
          classes_sum: 10,
          category: [],
        }
      },
      mounted() {
        //这里的this是vue中的this,当进入ajax之后,this就是ajax中的this,所以要先记录vue中的this
        var this_ = this
        if (document.cookie.length > 0) {
          var cStart = document.cookie.indexOf('token' + '=')
          if (cStart !== -1) {
            cStart = cStart + 'token'.length + 1
            var cEnd = document.cookie.indexOf(';', cStart)
            if (cEnd === -1) {
              cEnd = document.cookie.length
            }
            var token = unescape(document.cookie.substring(cStart, cEnd))
            $.ajax({
              type:"POST",
              async: false,
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              url:"http://localhost:8081/api/myinfo",
              beforeSend: function(request) {
                request.setRequestHeader("Authorization", "JWT "+token);
              },
              success:function (data) {
                if (data['code'] == -400) {
                  alert(data['message'])
                }
                else if (data['code'] == 0){
                  this_.username = data['data']['myinfo']['username']
                  this_.realname = data['data']['myinfo']['realname']
                  this_.useremail = data['data']['myinfo']['useremail']
                  this_.useraddress = data['data']['myinfo']['useraddress']
                  this_.e_coin = data['data']['myinfo']['e_coin']
                  this_.classes_num = data['data']['myinfo']['classes_num']
                  this_.category = data['data']['myinfo']['category']
                }
              },
              error:function (e) {
                alert("500")
              }
            });
          }
        }else{
          alert('获取token失败')
        }
      },
    }
</script>

<style lang="stylus" scoped>
</style>
