<template>
  <div>
    <i class="el-icon-rank">课程成员</i>
    <hr/>
    <el-button type="primary" plain @click="back_()">
      <i class="el-icon-back"></i>去上一级
    </el-button>
    <el-table
      :data="tableData.filter(data => !search || data.username.toLowerCase().includes(search.toLowerCase()))"
      style="width: 100%">
      <el-table-column
        label="用户ID"
        prop="user_id">
      </el-table-column>

      <el-table-column
        label="用户名"
        prop="username">
      </el-table-column>

      <el-table-column
        label="真实姓名"
        prop="realname">
      </el-table-column>

      <el-table-column
        label="邮箱"
        prop="useremail">
      </el-table-column>

      <el-table-column
        label="E-Coin"
        prop="e_coin">
      </el-table-column>

      <el-table-column align="right">
        <template slot="header" slot-scope="scope">
          <el-input
            v-model="search"
            size="mini"
            placeholder="输入关键字搜索"/>
        </template>
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="study_trace">查看学习详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      layout="prev, pager, next"
      :total="100">
    </el-pagination>
  </div>
</template>

<script>
    import $ from 'jquery'
    export default {
      name: "myClassMem.vue",
      data()  {
        return {
          classes_id: this.$route.params.classes_id,
          search: '',
          tableData: []
        }
      },
      mounted() {
        var this_ = this
        var request = {
          'classes_id': this.classes_id
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
              async: false,
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              data: JSON.stringify(request),
              url:"http://localhost:8081/api/myclassesmem",
              beforeSend: function(request) {
                request.setRequestHeader("Authorization", "JWT "+token);
              },
              success:function (data) {
                if (data['code'] == -400) {
                  alert(data['message'])
                }
                else if (data['code'] == 0){
                  this_.tableData = data['data']['users']
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
            path: `/myClass`,
          })
        },
        study_trace() {
          this.$router.push({
            name: 'studyTrace',
            params: {
              classes_id: this.classes_id
            }
          })
        },
      }
    }
</script>

<style scoped>

</style>
