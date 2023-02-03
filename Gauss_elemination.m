coeff_mat = input('Input coefficient matrix: ');
cons_mat = input('Input constant matrix: ');
if det(coeff_mat)== 0
  disp('This is not solvable')
else
  aug_mat = [coeff_mat cons_mat]
end

%%check for non zero diagonal elements and swap rows if the diagonal elements are zeroes

for i = 1:length(cons_mat)   #length of cons_mat is equal to the number of rows
  if aug_mat(i,i)== 0 && aug_mat(i+1,i)~=0
    x = aug_mat(i,:);
    aug_mat(i,:) = aug_mat(i+1,:);
    aug_mat(i+1,:)=x;
  elseif aug_mat(i,i)== 0 && aug_mat(i-1,i)~=0
    x = aug_mat(i,:);
    aug_mat(i,:) = aug_mat(i-1,:);
    aug_mat(i-1,:)=x;
  else
    continue
  endif
end

%%creating an upper triangular matrix by using row operations
for j = 1:length(cons_mat)
  k=j+1;
  while k <= length(cons_mat)
    if j>=k
      continue
    endif
    aug_mat(k,:) = aug_mat(k,:)-(aug_mat(k,j)/aug_mat(j,j))*aug_mat(j,:);
    k++;
  end
end

%% Solving for solutions by back substitution
y = zeros(1,length(cons_mat));
for i = length(cons_mat):-1:1
  y(i)= (aug_mat(i,end)-sum(aug_mat(i,i+1:end-1).*(y(i+1:end))))./aug_mat(i,i);
end

disp(["The solution is ", num2str(y)])
%%Verification using matrix inversion method
disp(["The solution using matrix inversion method ", mat2str((inv(coeff_mat)*cons_mat)')])

