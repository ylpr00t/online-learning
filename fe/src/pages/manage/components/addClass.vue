<template>
  <div id="c_container">

    <el-container>
      <el-main>
        <i class="el-icon-circle-plus-outline">新建课程</i>
        <hr/><br/>
        <el-row type="flex" justify="center">
          <el-col :span="2"><el-tag>课程名称:</el-tag></el-col>
          <el-col :span="8"><el-input v-model="name" placeholder="课程名"></el-input></el-col>
        </el-row>
        <br/>

        <el-row type="flex" justify="center">
          <el-col :span="2"><el-tag>课程说明:</el-tag></el-col>
          <el-col :span="8"><el-input
            type="textarea"
            :autosize="{ minRows: 4, maxRows: 6}"
            placeholder="请输入内容"
            v-model="explain"></el-input></el-col>
        </el-row>
        <br/>

        <el-row type="flex" justify="center">
          <el-col :span="2">
            <el-tag>课程分类:</el-tag>
          </el-col>
          <el-col :span="8">
            <el-select v-model="category" placeholder="请选择课程分类">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-col>
        </el-row>
        <br/>

        <el-row type="flex" justify="center">
          <el-col :span="2">
            <el-button type="primary" :span="4" @click="pushData()">提交数据</el-button>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
    import $ from 'jquery'
    export default {
      name: "addClass",
      data() {
        return {
          name: '',
          explain: '',
          options: [{
            value: 1,
            label: '计算机'
          }, {
            value: 2,
            label: '金融'
          }, {
            value: 3,
            label: '物理'
          }, {
            value: 4,
            label: '数学'
          }, {
            value: 5,
            label: '英语'
          }],
          category: 1
        }
      },
      methods: {
        pushData(){
          //检查参数
          if(this.name == "" || this.explain == "" || this.category == 0) {
            alert('以上参数不能为空')
            location.reload()
            return
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
              this.commit(token)
            }
          }else{
            alert('获取token失败')
            location.reload()
          }
        },
        commit(token){
          var request = {
            'name': this.name,
            'category': this.category,
            'explain': this.explain,
          }
          $.ajax({
            type:"POST",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(request),
            dataType: "json",
            url:"http://localhost:8081/api/addclasses",
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
      },
    }
</script>

<style lang="stylus" scoped>
  #c_container
    width 100%
    height 100%
    overflow hidden
    display: flex
    align-items center
    .c_center
      width 100%
      height 100%
      overflow auto
      align-items center
</style>
