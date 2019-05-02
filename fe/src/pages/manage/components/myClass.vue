<template>
    <div>
      <i class="el-icon-goods">我的课程</i>
      <hr/>
      <el-table
        :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%">

        <el-table-column
          label="ID"
          prop="id">
        </el-table-column>

        <el-table-column
          label="课程名"
          prop="name">
        </el-table-column>

        <el-table-column
          label="通行码"
          prop="rand_num">
        </el-table-column>

        <el-table-column
          label="建立时间"
          prop="create_date">
        </el-table-column>

        <el-table-column
          align="right">
          <template slot="header" slot-scope="scope">
            <el-input
              v-model="search"
              size="mini"
              placeholder="输入关键字搜索"/>
          </template>
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="handleEdit(scope.$index, scope.row)">课程资源</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">删除课程</el-button>
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
      name: "myClass",
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
              url:"http://localhost:8081/api/myclasses",
              beforeSend: function(request) {
                request.setRequestHeader("Authorization", "JWT "+token);
              },
              success:function (data) {
                if (data['code'] == -400) {
                  alert(data['message'])
                }
                else if (data['code'] == 0){
                  this_.tableData = data['data']['myclasses']
                  //console.log(this_.tableData)
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
      data()  {
        return {
          search: '',
          tableData: []
        }
      },
      methods: {
        handleEdit(index, row) {
          console.log(index, row, row.id);
          this.$router.push({
            name: 'myClassInfo',
            params: {
              classes_id: row.id
            }
          })
        },
        handleDelete(index, row) {
          console.log(index, row);
        },
      }
    }
</script>

<style scoped>

</style>
