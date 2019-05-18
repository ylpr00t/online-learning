<template>
    <div>
      <!--head-->
      <div>
        <el-button type="primary" plain @click="back_()">
          <i class="el-icon-back"></i>去上一级
        </el-button>
      </div><hr/>

      <!--text-->
      <div v-if="resource_type == 1">
        <div align="center">
          <span>{{resource_name}}</span><br/>
          <p>{{resource_content}}</p>
        </div>
      </div>

      <!--pic-->
      <div v-if="resource_type == 2">
        <div align="center">
          <span>{{resource_name}}</span><br/>
          <img :src="resource_content" height="300"/>
        </div>
      </div>

      <!--video-->
      <div v-if="resource_type == 3">
        <div align="center">
          <span>{{resource_name}}</span><br/>
          <video :src="resource_content" controls="controls" width="600px" height="400px">
            您的浏览器不支持 video 标签。
          </video>
        </div>
      </div>

    </div>
</template>

<script>
    import $ from 'jquery'
    export default {
      name: "resourceShow",
      data() {
        return {
          resource_id: this.$route.params.resource_id,
          classes_id: this.$route.params.classes_id,
          resource_name: this.$route.params.resource_name,
          resource_type: this.$route.params.resource_type,
          resource_content: this.$route.params.resource_content,
        }
      },
      created() {
        //这里的this是vue中的this,当进入ajax之后,this就是ajax中的this,所以要先记录vue中的this
        var request = {
          'classes_id': this.classes_id,
          'resource_id': this.resource_id
        }
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
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              data: JSON.stringify(request),
              url:"http://localhost:8081/api/update_ecoin",
              beforeSend: function(request) {
                request.setRequestHeader("Authorization", "JWT "+token);
              },
              success:function (data) {
                if (data['code'] == -400) {
                  alert(data['message'])
                }
                else if (data['code'] == 0){
                  console.log('update_ecoin success')
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
      methods: {
        back_() {
          this.$router.push({
            name: 'resourceInfo',
            params: {
              classes_id: this.classes_id
            }
          })
        }
      }
    }
</script>

<style scoped>

</style>
