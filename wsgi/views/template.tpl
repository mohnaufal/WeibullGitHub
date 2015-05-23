<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Weibull Parameter Estimator 1.1</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="">

	<!--link rel="stylesheet/less" href="less/bootstrap.less" type="text/css" /-->
	<!--link rel="stylesheet/less" href="less/responsive.less" type="text/css" /-->
	<!--script src="js/less-1.3.3.min.js"></script-->
	<!--append ‘#!watch’ to the browser URL, then refresh the page. -->
	
	<link href="/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="/static/css/style.css" rel="stylesheet">

  <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
  <!--[if lt IE 9]>
    <script src="js/html5shiv.js"></script>
  <![endif]-->

  <!-- Fav and touch icons -->
  <link rel="apple-touch-icon-precomposed" sizes="144x144" href="/static/img/apple-touch-icon-144-precomposed.png">
  <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/static/img/apple-touch-icon-114-precomposed.png">
  <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/static/img/apple-touch-icon-72-precomposed.png">
  <link rel="apple-touch-icon-precomposed" href="/static/img/apple-touch-icon-57-precomposed.png">
  <link rel="shortcut icon" href="/static/img/favicon.png">
  
	<script type="text/javascript" src="/static/js/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="/static/js/scripts.js"></script>
</head>

<body style="background:#ddd">
<div class="container" style="background:#fff">
	<div class="row clearfix">
		<div class="col-md-12 column">
			<h3 class="text-center" style="background:#0ae">
				<br><br>WEIBULL PARAMETER ESTIMATOR<br><br>Ver. 1.1<br><br>
			</h3>
			<div class="tabbable" id="tabs-380333">
				<ul class="nav nav-tabs">
					<li class="active">
						<a href="#panel-480560" data-toggle="tab">Home</a>
					</li>
					<li>
						<a href="#panel-841589" data-toggle="tab">Manual Input</a>
					</li>
					<li>
						<a href="#panel-filinput" data-toggle="tab">File Input</a>
					</li>
					<li>
						<a href="#panel-about" data-toggle="tab">About</a>
					</li>
				</ul>
				<div class="tab-content">
					<div class="tab-pane active" id="panel-480560">
						<p>
							<br>
							This web provides an application for calculating the shape parameter, scale parameter and location parameter from the weibull distribution. <br> Weibull Parameter will be used for building four main weibull function, Probability Density Function (PDF), Cumulative Distribution Function (CDF), Failure Rate and Reliability. <br> This web also provide Reliability to Reliable life converter and vice versa. <br>
							For further reading, please click one of the references below<br>
							<a href="http://en.wikipedia.org/wiki/Weibull_distribution"> 
							  Weibull Distribution on Wikipedia
							</a>
							<br>
							<a href="http://reliawiki.org/index.php/The_Weibull_Distribution"> 
							  Weibull Distribution on Reliawiki.org 
							</a>
							<br>
							<br>
							Terms for input data:<br>
							- Input data should not be less than 4  failure data. otherwise this app will not be able to compute the results.<br>
							- Enter only number for input, if any alphabetical letter this app will not be able to compute the results.<br>
							- Input data must be sorted from smallest to largest.<br>
							- For File Input, this application can only read .csv file extension (Comma separated Value). User can convert file which contain failure data in spreadsheet based application such as Microsoft Excel. Failure data should be sorted into a single column. You can download example csv files
							<a href="/static/example.csv">
								here
							</a>
							<br>
							- The method used in this application allows user to input up to 30 failure data. If it exceeds the results will still appear, but will reduce the accuracy of the results. Please use another method to calculate the parameters of the weibull distribution for larger quantities of failure data.
							<br>
							<br>
						</p>
					</div>
					<div class="tab-pane" id="panel-841589">
						<p>
							<br>
							This section provide input form for failure data. Enter failure data and press Submit.
							<br>
						</p>
						<form method = "post" enctype="multipart/form-data" action= "/fitting" target ="_blank">
							<table border ="1">
								<thead>
									<tr>
										<th>Failure Time</th>
									</tr>
								</thead>	
								<tr>
									<td><textarea rows ="50" cols = "20" name ="inputdata"></textarea>
									<button type="submit" class="btn btn-default">Submit</button>
								</tr>
							</table>
						</form>
					</div>
					<div class="tab-pane" id="panel-filinput">
						<p>
							<br>
							This section provide input file in .csv extension which contains failure data. 
							<br>
						</p>
						<form role="form" method="post" enctype= "multipart/form-data" action="/fitting?upload=1" target="_blank">

						<div class="form-group">
							 <label for="exampleInputFile">File input</label><input type="file" name= "inputfile" id="exampleInputFile">

						</div>
						<button type="submit" class="btn btn-default">Submit</button>
						</form>
					</div>
					<div class="tab-pane" id="panel-about">
						<p>
							<br>
							This web app only use for academic purpose. 
							<br> 
							If you have any thoughts please kindly share with me. 
							<br>
							 I'll gladly reply all of your thoughts. 
							<br>
							<br>
							Mohammad Naufal 
							<br>
							mnaufal92@gmail.com
							<br> 
							Aeronautics and Astronautics Engineering 
							<br> 
							Faculty of Mechanical and Aerospace Engineering 
							<br>
							Bandung Institute of Technology
							<br>
					</div>
				</div>
				<h5 class="text-center" style="background:#000;color:#fff">
				<br>
				<br>
				weibparest-naufal.rhcloud.com
				<br>
				<br>Copyright 2015
				<br>Faculty of Mechanical and Aerospace Engineering
				<br>Bandung Institute of Technology
				<br><br>
				</h5>
			</div>
		</div>
	</div>
</div>
</body>
</html>
