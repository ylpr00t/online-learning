<template>
  <div>
    <i class="el-icon-rank">学习追踪</i>
    <hr/>
    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        label="追踪ID"
        prop="trace_id">
      </el-table-column>

      <el-table-column
        label="追踪ECOIN"
        prop="trace_ecoin">
      </el-table-column>

      <el-table-column
        label="追踪详情"
        prop="trace_info">
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
      name: "studyTrace.vue",
      data()  {
        return {
          user_id: this.$route.params.user_id,
          classes_id: this.$route.params.classes_id,
          tableData: []
        }
      },
      mounted() {
        var this_ = this
        var request = {
          'user_id': this.user_id,
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
              url:"http://localhost:8081/api/study_trace",
              beforeSend: function(request) {
                request.setRequestHeader("Authorization", "JWT "+token);
              },
              success:function (data) {
                if (data['code'] == -400) {
                  alert(data['message'])
                }
                else if (data['code'] == 0){
                  this_.tableData = data['data']['trace_info']
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
      }
    }
</script>

<style scoped>

</style>
