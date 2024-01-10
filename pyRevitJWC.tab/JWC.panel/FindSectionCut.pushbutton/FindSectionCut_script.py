orderedParameters = el.GetOrderedParameters()

for parameter in orderedParameters:
	print(parameter.Definition.Name)
	print(parameter.AsString())