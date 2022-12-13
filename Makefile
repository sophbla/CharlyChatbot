reinstall_package:
	@pip uninstall -y project_mhconvai || :
	@pip install -e .

# What is the use of this? Here we run the function with the default parameter, which are empty strings.
# I just adapted this from the taxifare package...

run_pred:
	python -c 'from project_mhconvai.interface.main import predict_with_filters; predict_with_filters()'

run_api:
	uvicorn project_mhconvai.api.fast:app --reload
