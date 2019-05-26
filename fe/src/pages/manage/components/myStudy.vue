<template>
    <div>
      <el-row>
        <el-col :span="6">
          <i class="el-icon-goods">我的学习</i>
        </el-col>
        <el-col :span="5" style="float: right">
          <el-button type="primary" plain @click="dialogVisible = true" style="float: right">
            <i class="el-icon-circle-plus-outline"></i>添加学习
          </el-button>
          <el-dialog
            title="添加学习"
            :visible.sync="dialogVisible"
            width="35%">
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
              <el-form-item label="课程通行码" prop="rand_num">
                <el-input v-model="ruleForm.rand_num"></el-input>
              </el-form-item>
              <el-form-item label="课程备注" prop="explain">
                <el-input v-model="ruleForm.explain"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="dialogVisible=false;submitForm('ruleForm')">确认添加</el-button>
                <el-button @click="resetForm('ruleForm')">重置</el-button>
              </el-form-item>
            </el-form>
          </el-dialog>
        </el-col>
      </el-row>
      <hr/>

      <el-row>
        <el-table
          :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
          style="width: 100%">

          <!--
          <el-table-column
            label="学习ID"
            prop="classes_id">
          </el-table-column>
          -->

          <el-table-column
            label="课程名称"
            prop="name">
          </el-table-column>

          <!--
          <el-table-column
            label="课程分类"
            prop="category">
          </el-table-column>
          -->

          <el-table-column
            label="课程所有者"
            prop="username">
          </el-table-column>

          <el-table-column
            label="获得ECOIN"
            prop="e_coin">
          </el-table-column>

          <el-table-column
            label="课程备注"
            prop="explain">
          </el-table-column>

          <el-table-column
            label="添加时间"
            prop="create_time">
          </el-table-column>

          <el-table-column
            align="right">
            <!--
            <template slot="header" slot-scope="scope">
              <el-input
                v-model="search"
                size="mini"
                placeholder="输入关键字搜索"/>
            </template>
            -->
            <template slot-scope="scope">
              <el-button
                size="mini"
                @click="classes_resource(scope.$index, scope.row)">查看课程资源
              </el-button>
              <el-button
                size="mini"
                @click="study_trace(scope.$index, scope.row)">查看学习记录
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
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
        name: "myStudy",
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
                url:"http://localhost:8081/api/mystudy",
                beforeSend: function(request) {
                  request.setRequestHeader("Authorization", "JWT "+token);
                },
                success:function (data) {
                  if (data['code'] == -400) {
                    alert(data['message'])
                  }
                  else if (data['code'] == 0){
                    this_.tableData = data['data']['mystudys']
                    if(data['data']['mystudys']['category'] == 1)
                      this_.tableData['category'] = "计算机"
                    if(data['data']['mystudys']['category'] == 2)
                      this_.tableData['category'] = "金融"
                    if(data['data']['mystudys']['category'] == 3)
                      this_.tableData['category'] = "物理"
                    if(data['data']['mystudys']['category'] == 4)
                      this_.tableData['category'] = "数学"
                    if(data['data']['mystudys']['category'] == 5)
                      this_.tableData['category'] = "英语"
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
        data() {
          return {
            search: '',
            dialogVisible: false,
            tableData: [],
            ruleForm: {
              rand_num: '',
              explain: '',
            },
            rules: {
              rand_num: [
                {required: true, message: '请输入课程通信码', trigger: 'blur'},
                {min: 6, max: 6, message: '长度为6', trigger: 'blur'}
              ],
              explain: [
                {required: true, message: '请输入课程备注', trigger: 'blur'},
                {min: 1, max: 50, message: '长度为1-50', trigger: 'blur'}
              ],
            }
          }
        },
        methods: {
          classes_resource(index, row) {
            this.$router.push({
              name: 'resourceInfo',
              params: {
                classes_id: row.classes_id
              }
            })
          },
          study_trace(index, row) {
            this.$router.push({
              name: 'studyTrace2',
              params: {
                user_id: row.user_id,
                classes_id: row.classes_id
              }
            })
          },
          submitForm(formName) {
            this.$refs[formName].validate((valid) => {
              if (valid) {
                //这里的this是vue中的this,当进入ajax之后,this就是ajax中的this,所以要先记录vue中的this
                var this_ = this
                var request = {
                  'rand_num': this.ruleForm.rand_num,
                  'explain': this.ruleForm.explain,
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
                      url:"http://localhost:8081/api/addstudy",
                      beforeSend: function(request) {
                        request.setRequestHeader("Authorization", "JWT "+token);
                      },
                      success:function (data) {
                        if (data['code'] == -400) {
                          alert(data['message'])
                        }
                        else if (data['code'] == 0){
                          alert(data['message'])
                          location.reload()
                        }
                      },
                      error:function (e) {
                        alert("500")
                      }
                    });
                  }
                }else {
                  alert('获取token失败')
                }
              } else {
                console.log('error submit!!');
                return false;
              }
            });
          },
          resetForm(formName) {
            this.$refs[formName].resetFields();
          },
          deleteRes(index, row) {

          }
        },
    }
</script>

<style scoped>

</style>
