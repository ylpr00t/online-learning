<template>
    <div >
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="真实姓名">
          <el-input style="width: 50%" v-model="realname" placeholder="请输入真实姓名"></el-input>
        </el-form-item>
        <el-form-item label="电子邮箱">
          <el-input style="width: 50%" v-model="useremail" placeholder="请输入电子邮箱"></el-input>
        </el-form-item>
        <el-form-item label="详细地址">
          <el-input style="width: 50%" v-model="useraddress" placeholder="请输入通信地址"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">提交数据</el-button>
        </el-form-item>
      </el-form>
    </div>
</template>

<script>
    import $ from 'jquery'
    export default {
      name: "set",
      data() {
        return {
          realname: '',
          useremail: '',
          useraddress: ''
        }
      },
      methods: {
        checkArgs_(){
          if(this.realname == "" || this.useremail == "" || this.useraddress == ""){
            alert('以上参数不能为空')
            location.reload()
            return -1;
          }
          return 0;
        },
        getCookie_(){
          if(document.cookie.length > 0) {
            var cStart = document.cookie.indexOf('token' + '=')
            if(cStart != 1){
              cStart = cStart + 'token'.length + 1
              var cEnd = document.cookie.indexOf(';', cStart)
              if(cEnd == -1){
                cEnd = document.cookie.length
              }
              var token = unescape(document.cookie.substring(cStart, cEnd))
              return token
            }
          } else {
            return ''
          }
        },
        commit_(token){
          var request = {
            'realname': this.realname,
            'useremail': this.useremail,
            'useraddress': this.useraddress,
          }
          $.ajax({
            type:"POST",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(request),
            dataType: "json",
            url:"http://127.0.0.1:8081/api/setting",
            beforeSend: function(request) {
              request.setRequestHeader("Authorization", "JWT "+token);
            },
            success:function (data) {
              if (data['code'] == -400) {
                alert(data['message'])
                location.reload()
              }
              else if (data['code'] == 0){
                alert(data['message'])
                location.reload()
              }
            },
            error:function (e) {
              alert("500")
              location.reload()
            }
          });
        },
        onSubmit() {
          //检查参数
          if(this.checkArgs_() == -1)
            return
          var token = this.getCookie_()
          if (token != '') {
            this.commit_(token)
          }else{
            alert('获取token失败')
            location.reload()
          }
        },
      }
    }
</script>

<style scoped>

</style>
