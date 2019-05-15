<template>

  <div>
    <i class="el-icon-goods">课程资料</i>
    <hr/>
    <div>
      <br/>
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
                @click="handleEdit(scope.$index, scope.row)">查看详情</el-button>
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
            }
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
          handleEdit(index, row) {
            console.log(index, row, row.id);
          },
          handleClose(done) {
            this.$confirm('确认关闭？')
              .then(_ => {
              done();
            })
            .catch(_ => {});
          },
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
