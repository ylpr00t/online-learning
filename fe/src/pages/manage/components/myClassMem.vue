<template>
  <div>
    <el-row>
      <el-col :span="6">
        <i class="el-icon-rank">课程成员</i>
      </el-col>
      <el-col :span="2.5" style="float: right">
        <el-button type="primary" plain @click="dialogVisible = true">
          <i class="el-icon-check"></i>导出成绩
        </el-button>
        <el-dialog
            title="导出学员成绩"
            :visible.sync="dialogVisible"
            width="35%">
            <el-form label-width="100px" class="demo-ruleForm">
              <el-form-item label="本课程总分">
                <el-input v-model="sum_score"></el-input>
              </el-form-item>
              <el-form-item label="开启五级制">
                <el-select v-model="five_level" placeholder="请选择">
                  <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="dialogVisible=false;export_score()">生成并导出</el-button>
              </el-form-item>
            </el-form>
        </el-dialog>
      </el-col>
    </el-row>
    <hr/>

    <el-row>
      <el-col>
        <el-button type="primary" plain @click="back_()">
          <i class="el-icon-back"></i>去上一级
        </el-button>
      </el-col>
    </el-row>

    <el-row>
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
              @click="study_trace(scope.$index, scope.row)">查看学习详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        layout="prev, pager, next"
        :total="100">
      </el-pagination>
    </el-row>
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
          tableData: [],
          dialogVisible: false,
          sum_score: 100,
          five_level: 0,
          options: [{
            value: 1,
            label: '是'
          }, {
            value: 0,
            label: '否'
          }],
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
        export_score() {
          var this_ = this
          var request = {
            'sum_score': this.sum_score,
            'five_level': this.five_level,
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
                url:"http://localhost:8081/api/exportscore",
                beforeSend: function(request) {
                  request.setRequestHeader("Authorization", "JWT "+token);
                },
                success:function (data) {
                  if (data['code'] == -400) {
                    alert(data['message'])
                  }
                  else if (data['code'] == 0){
                    var filename = data['data']['filename']
                    var url = "http://localhost:8080/" + filename
                    //请求文件名，打开新窗口
                    window.open(url, "_blank")
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
        study_trace(index, row) {
          this.$router.push({
            name: 'studyTrace',
            params: {
              user_id: row.user_id,
              classes_id: this.classes_id
            }
          })
        },
      }
    }
</script>

<style scoped>

</style>
