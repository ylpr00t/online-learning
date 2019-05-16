<template>

  <div>
    <i class="el-icon-goods">课程资料</i>
    <hr/>
    <div>
      <el-row>
        <el-button type="primary" plain @click="back()">
          <i class="el-icon-back"></i>去上一级
        </el-button>
        <el-button type="primary" plain @click="dialogVisible = true">
          <i class="el-icon-circle-plus-outline"></i>添加资料
        </el-button>

        <el-dialog
          title="添加资料"
          :visible.sync="dialogVisible"
          width="45%"
          :before-close="handleClose">
          <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="资源分类">
              <el-button @click="resourceType=1; resetForm('ruleForm')">文本</el-button>
              <el-button @click="resourceType=2; resetForm('ruleForm')">图片</el-button>
              <el-button @click="resourceType=3; resetForm('ruleForm')">视频</el-button>
            </el-form-item>
            <el-form-item label="资源名称" prop="name">
              <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="资源说明" prop="desc">
              <el-input type="textarea" v-model="ruleForm.desc"></el-input>
            </el-form-item>

            <div v-if="resourceType === 1">
              <el-form-item label="资源内容" prop="content">
                <el-input type="textarea" v-model="ruleForm.content" :autosize="{ minRows: 5, maxRows: 50}"></el-input>
              </el-form-item>
            </div>

            <div v-else-if="resourceType === 2">
              <el-form-item label="图片文件" prop="content">
                <el-upload
                  class="upload-demo"
                  action="http://localhost:8081/api/upload"
                  drag
                  multiple
                  :show-file-list="true"
                  :data={resource_type:2}
                  :on-success="upload_success"
                  :on-error="upload_error">
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">将图片拖到此处，或<em>点击上传</em></div>
                  <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
                </el-upload>
              </el-form-item>
            </div>

            <div v-else-if="resourceType === 3">
              <el-form-item label="视频文件" prop="content">
                <el-upload
                  class="upload-demo"
                  action="http://localhost:8081/api/upload"
                  drag
                  multiple
                  :show-file-list="true"
                  :data={resource_type:3}
                  :on-success="upload_success"
                  :on-error="upload_error">
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">将视频拖到此处，或<em>点击上传</em></div>
                  <div class="el-upload__tip" slot="tip">只能上传mp4/avi文件，且不超过500kb</div>
                </el-upload>
              </el-form-item>
            </div>
            <el-form-item>
              <el-button type="primary" @click="dialogVisible=false;submitForm('ruleForm')">立即创建</el-button>
              <el-button @click="resourceType=1; resetForm('ruleForm')">重置数据</el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
      </el-row><br/>

      <el-row>
        <el-table
          :data="tableData"
          style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="资料名称">
                  <span>{{ props.row.name }}</span>
                </el-form-item><br/>
                <el-form-item label="资料描述">
                  <span>{{ props.row.desc }}</span>
                </el-form-item><br/>
                <el-form-item label="资料详情">
                  <span>{{ props.row.content }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>

          <el-table-column
            label="资料编号"
            prop="id">
          </el-table-column>
          <el-table-column
            label="资料名称"
            prop="name">
          </el-table-column>
          <el-table-column
            label="资料描述"
            prop="desc">
          </el-table-column>
          <el-table-column
            label="创建时间"
            prop="create_time">
          </el-table-column>

          <el-table-column
            align="right">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)">删除资源</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </div>
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
        name: "myClassInfo",
        data() {
          return {
            classes_id: this.$route.params.classes_id,
            dialogVisible: false,
            resourceType: 1,
            tableData: [],
            ruleForm: {
              name: '',
              desc: '',
              content: '',
            },
            rules: {
              name: [
                { required: true, message: '请输入资源名称', trigger: 'blur' },
                { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
              ],
              category: [
                { required: true, message: '请选择资源分类', trigger: 'change' }
              ],
              desc: [
                { required: true, message: '请填写资源描述', trigger: 'blur' }
              ],
              content: [
                { required: true, message: '请填写资源内容' }
              ]
            },
          }
        },
        mounted() {
          //这里的this是vue中的this,当进入ajax之后,this就是ajax中的this,所以要先记录vue中的this
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
                url:"http://localhost:8081/api/myresources",
                beforeSend: function(request) {
                  request.setRequestHeader("Authorization", "JWT "+token);
                },
                success:function (data) {
                  if (data['code'] == -400) {
                    alert(data['message'])
                  }
                  else if (data['code'] == 0){
                    this_.tableData = data['data']['myresources']
                    console.log(this_.tableData)
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
          back(){
            this.$router.push({
              path: `/myClass`,
            })
          },
          handleEdit(index, row) {
            console.log(index, row, row.id);
          },
          handleDelete(index, row) {
            //console.log(index, row);
            var request = {
              'resource_id': row.id
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
                  url:"http://localhost:8081/api/deleteresource",
                  beforeSend: function(request) {
                    request.setRequestHeader("Authorization", "JWT "+token);
                  },
                  success:function (data) {
                    if (data['code'] == -400) {
                      alert(data['message'])
                    } else if (data['code'] == 0){
                      alert(data['message'])
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
          handleClose(done) {
            this.$confirm('确认关闭？')
              .then(_ => {
              done();
            })
            .catch(_ => {});
          },
          submitForm(formName) {
            this.$refs[formName].validate((valid) => {
              if (valid) {
                //这里的this是vue中的this,当进入ajax之后,this就是ajax中的this,所以要先记录vue中的this
                var this_ = this
                if(this.ruleForm.content == '') {
                  alert('内容为空或文件上传失败')
                  return
                }
                var request = {
                  'classes_id': this.classes_id,
                  'name': this.ruleForm.name,
                  'category': 0,
                  'desc': this.ruleForm.desc,
                  'content': this.ruleForm.content
                }
                if(this.resourceType == 1)
                  request.category = 1
                else if(this.resourceType == 2)
                  request.category = 2
                else if(this.resourceType == 3)
                  request.category = 3
                else
                  request.category = 0
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
                      url:"http://localhost:8081/api/addresource",
                      beforeSend: function(request) {
                        request.setRequestHeader("Authorization", "JWT "+token);
                      },
                      success:function (data) {
                        if (data['code'] == -400) {
                          alert(data['message'])
                        }
                        else if (data['code'] == 0){
                          alert(data['message'])
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
          upload_success(res, file) {
            this.ruleForm.content = res['data']['filename']
            //alert(res['message'] + res['data']['filename'])
          },
          upload_error(res, file) {
            this.ruleForm.content = ''
          }
        }
    }
</script>

<style>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
